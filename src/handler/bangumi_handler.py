from ast import TypeVar
import os
from typing import Any, Iterable, Type, Callable
from pathlib import Path
from proto_py.bangumi.bangumi_pb2 import Episode, BangumiData, Name, Bangumi, BangumiIndex
from proto_py.base.resources_pb2 import ExternalResource
from proto_py.base.language_code_pb2 import LanguageCode
from google.protobuf import json_format
from google.protobuf.message import Message


NameAlreadyExist = Exception("bangumi name already exist")
BangumiNotExist = Exception("bangumi not exist")
BangumiAlreadyExist = Exception("bangumi already exist")
UnsupportedExternalResource = Exception("unsupported external resource")


class BangumiHandler():
    storage_path = ""
    bangumi_index = BangumiIndex()

    def __init__(self, storage_path: str) -> None:
        self.storage_path = storage_path
        try:
            original_umask = os.umask(0)
            Path(storage_path).mkdir(0o755, exist_ok=True)
        finally:
            os.umask(original_umask)
        if not self.get_bangumi_index_file_path().exists():
            self.save_bangumi_index_file()
        else:
            self.load_bangumi_index_file()

    def merge_bangumi_episodes(self, bangumi: BangumiData, episodes: Iterable[Episode]) -> BangumiData:
        result: BangumiData = BangumiData()
        result.CopyFrom(bangumi)
        for episode in episodes:
            exists_episodes = tuple(
                filter(lambda x: x.index == episode.index, result.episodes))
            if len(exists_episodes) == 0:
                result.episodes.append(episode)
            else:
                exists_episode: Episode = exists_episodes[0]
                merge_result = self.merge_episodes_external_resources(
                    exists_episode, episode.resources)
                exists_episode.CopyFrom(merge_result)
        return result

    def merge_episodes_external_resources(
            self,
            episode: Episode,
            external_resources: Iterable[ExternalResource],
    ) -> Episode:
        result: Episode = Episode()
        result.CopyFrom(episode)
        for resource in external_resources:
            resources_type = resource.WhichOneof("resources")
            # magnet
            # website
            # share_dmhy_org
            same_resources = None
            exists_resources = filter(lambda x: x.WhichOneof(
                "resources") == resources_type, result.resources)

            if resources_type == "magnet":
                same_resources = tuple(filter(
                    lambda x: x.magnet.url == resource.magnet.url, exists_resources))
            elif resources_type == "website":
                same_resources = tuple(filter(
                    lambda x: x.website.url == resource.website.url, exists_resources))
            elif resources_type == "share_dmhy_org":
                same_resources = tuple(filter(lambda x: x.share_dmhy_org.magnet.url ==
                                              resource.share_dmhy_org.magnet.url, exists_resources))
            else:
                continue

            if len(same_resources) == 0:
                result.resources.append(resource)
            else:
                exist_resource: ExternalResource = same_resources[0]
                # using MergeFrom to keep external meta
                exist_resource.CopyFrom(resource)

                # if resources_type == "share_dmhy_org":
                #     deduped_array = BangumiHandler.deduplicate(
                #         exist_resource.share_dmhy_org.tags, lambda x: x.tag)
                #     del exist_resource.share_dmhy_org.tags[:]
                #     exist_resource.share_dmhy_org.tags.extend(deduped_array)


        return result

    def load_bangumi_data(self, bangumi_id: int) -> BangumiData:
        raw_str = self.read_bangumi_data_file(bangumi_id=bangumi_id)
        bangumi = BangumiData()
        json_format.Parse(raw_str, bangumi)
        return bangumi

    def read_bangumi_data_file(self, bangumi_id: int) -> str:
        assert bangumi_id != 0
        with open(self.get_bangumi_data_file_path(bangumi_id), "r") as f:
            return f.read()

    def write_bangumi_data_file(self, bangumi: BangumiData):
        assert bangumi.bangumi_id != 0
        bangumi = self.format_bangumi_data(bangumi)
        json_str = json_format.MessageToJson(
            bangumi,
            including_default_value_fields=False,
            preserving_proto_field_name=True,
            indent=4,
            ensure_ascii=False,
        )
        save_dir = self.get_bangumi_data_file_dir(bangumi.bangumi_id)
        try:
            original_umask = os.umask(0)
            save_dir.mkdir(0o755, exist_ok=True)
        finally:
            os.umask(original_umask)
        with open(str(self.get_bangumi_data_file_path(bangumi.bangumi_id)), "w") as f:
            f.write(json_str)

    def save_bangumi_index_file(self):
        self.bangumi_index.index.sort(key=lambda x: x.id)
        json_str = json_format.MessageToJson(
            self.bangumi_index,
            including_default_value_fields=False,
            preserving_proto_field_name=True,
            indent=4,
            ensure_ascii=False,
        )
        with open(self.get_bangumi_index_file_path(), "w") as f:
            f.write(json_str)

    def load_bangumi_index_file(self) -> BangumiIndex:
        with open(self.get_bangumi_index_file_path(), "r") as f:
            json_str = f.read()
        json_format.Parse(
            json_str, self.bangumi_index
        )
        return self.bangumi_index

    def get_bangumi_index_file_path(self) -> Path:
        return Path(self.storage_path, "index.json")

    def get_bangumi_data_file_dir(self, bangumi_id: int) -> Path:
        return Path(self.storage_path, str(bangumi_id))

    def get_bangumi_data_file_path(self, bangumi_id: int) -> Path:
        return Path(self.get_bangumi_data_file_dir(bangumi_id), "data.json")

    def is_bangumi_id_exists(self, bangumi_id: int) -> bool:
        try:
            self.get_bangumi_by_id(bangumi_id=bangumi_id)
        except Exception as e:
            if e is BangumiNotExist:
                return False
            else:
                raise e
        return True

    def create_bangumi(self, bangumi_id: int, bangumi_name: str, bangumi_name_lang: str, series_id: int = 0) -> BangumiData:
        if self.is_bangumi_id_exists(bangumi_id):
            raise BangumiAlreadyExist

        for exist_bangumi_id in self.list_bangumi_ids():
            exist_bangumi, _ = self.get_bangumi_by_id(exist_bangumi_id)
            same_names = tuple(
                filter(
                    lambda x: x.name.strip().lower() == bangumi_name.strip().lower(),
                    exist_bangumi.names
                )
            )
            if len(same_names) > 0:
                raise NameAlreadyExist
        bangumi = Bangumi(
            id=bangumi_id,
            series_id=series_id,
            names=[
                Name(
                    language_code=LanguageCode.Value(bangumi_name_lang),
                    name=bangumi_name
                )
            ]
        )
        self.bangumi_index.index.append(bangumi)
        self.write_bangumi_data_file(BangumiData(bangumi_id=bangumi_id))
        self.save_bangumi_index_file()
        return bangumi

    def get_bangumi_by_id(self, bangumi_id: int) -> tuple[Bangumi, BangumiData]:
        bangumis = tuple(
            filter(
                lambda x: x.id == bangumi_id,
                self.bangumi_index.index,
            )
        )
        if len(bangumis) == 0:
            raise BangumiNotExist
        bangumi_data = self.load_bangumi_data(bangumi_id)
        return bangumis[0], bangumi_data
    
    def get_bangumi_id_by_name(self, bangumi_name: str) -> int:
        for index in self.bangumi_index.index:
            same_names = tuple(
                filter(
                    lambda x: x.name == bangumi_name,
                    index.names,
                )
            )
            if len(same_names) > 0:
                return index.id
        return 0

    def add_bangumi_name(self, bangumi_id: int, bangumi_name: str, bangumi_name_lang: str):
        bangumi, _ = self.get_bangumi_by_id(bangumi_id)

        new_name = Name(
            language_code=LanguageCode.__members__[bangumi_name_lang],
            name=bangumi_name
        )

        assert len(
            tuple(
                filter(
                    lambda x: x.name.strip().lower() == new_name.name.strip().lower(),
                    bangumi.names,
                )
            )
        ) == 0, NameAlreadyExist

        bangumi.names.append(new_name)
        bangumi.names.sort(key=lambda x: x.name)
        self.save_bangumi_index_file()

    def list_bangumi_ids(self):
        bangumi_ids = [item.id for item in self.bangumi_index.index]
        return bangumi_ids

    @staticmethod
    def format_bangumi_data(bangumi: BangumiData, inplace=True) -> BangumiData:
        if inplace is True:
            result = bangumi
        else:
            result = BangumiData()
            result.CopyFrom(bangumi)

        result.episodes.sort(key=lambda x: x.index)
        deduped_array = BangumiHandler.deduplicate(
            result.episodes, lambda x: x.index)
        del result.episodes[:]
        result.episodes.extend(deduped_array)
        for episode in result.episodes:
            BangumiHandler.format_episode(episode, inplace=inplace)
        return bangumi

    @staticmethod
    def format_episode(epidose: Episode, inplace=True) -> Episode:
        if inplace is True:
            result = epidose
        else:
            result = Episode()
            result.CopyFrom(epidose)

        result.resources.sort(
            key=BangumiHandler.get_external_resources_sort_key)
        deduped_array = BangumiHandler.deduplicate(
            result.resources, BangumiHandler.get_external_resources_sort_key)
        del result.resources[:]
        result.resources.extend(deduped_array)

        for resource in result.resources:
            BangumiHandler.format_external_resources(
                resource, inplace=inplace)
        return result

    @staticmethod
    def format_external_resources(resource: ExternalResource, inplace=True) -> ExternalResource:
        if inplace is True:
            result = resource
        else:
            result = ExternalResource()
            result.CopyFrom(resource)
        if resource.HasField("share_dmhy_org"):
            resource.share_dmhy_org.tags.sort(key=lambda x: x.tag)
            deduped_array = BangumiHandler.deduplicate(
                resource.share_dmhy_org.tags, lambda x: x.tag)
            del resource.share_dmhy_org.tags[:]
            resource.share_dmhy_org.tags.extend(deduped_array)
        return result

    @staticmethod
    def get_external_resources_sort_key(resource: ExternalResource) -> str:
        resources_type = resource.WhichOneof("resources")
        if resources_type == "magnet":
            return resource.magnet.url
        elif resources_type == "website":
            return resource.website.url
        elif resources_type == "share_dmhy_org":
            return resource.share_dmhy_org.page_link
        else:
            raise UnsupportedExternalResource

    @staticmethod
    def deduplicate(inputs: Iterable[Message], compare_key: Callable[[Message], Any]) -> Iterable[Message]:
        unique_values = set()
        new_array = []
        for item in inputs:
            key = compare_key(item)
            if key not in unique_values:
                unique_values.add(key)
                new_array.append(item)
        return new_array
