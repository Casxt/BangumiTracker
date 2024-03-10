from typing import Iterable
import aiohttp
from proto_py.tracker import share_dmhy_org_pb2
from proto_py.bangumi import bangumi_pb2
from proto_py.base import language_code_pb2, resources_pb2, tag_pb2
from google.protobuf import json_format
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode

import re



RedunantConfigKeyExpection = Exception("config key already exists")
HTTPNot200Expection = Exception("http status code is not 200")

class ShareDMHYTrackerHandler():
    rss_config = share_dmhy_org_pb2.SHARE_DMHY_ORG_TRACKER()
    rss_config_path = ""
    def __init__(self, config_path: str) -> None:
        self.rss_config_path = config_path
        self.rss_config = self.load_config(config_path)
    
    def add_config(self, key: str, bangumi_id: int, rss_url: str):
        assert key != ""
        assert rss_url != ""
        for config in self.rss_config.configs:
            if config.key == key:
                raise RedunantConfigKeyExpection
        self.rss_config.configs.append(share_dmhy_org_pb2.SHARE_DMHY_ORG_TRACKER_CONFIG(
            key=key,
            bangumi_id=bangumi_id,
            rss_url=rss_url,
        ))
        self.save_config()
    
    def delete_config(self, key: str):
        assert key != ""
        self.rss_config.configs[:] = [x for x in self.rss_config.configs if x.key != key]

    def config_to_json(self) -> str:
        return json_format.MessageToJson(
            self.rss_config, 
            preserving_proto_field_name=True, 
            including_default_value_fields=False, 
            indent=4,
            ensure_ascii=False,
            )
        
    def save_config(self):
        assert self.rss_config_path != ""
        json_str = self.config_to_json()
        with open(self.rss_config_path, "w") as config:
            config.write(json_str)

    def load_config(self, config_path: str) -> share_dmhy_org_pb2.SHARE_DMHY_ORG_TRACKER:
        assert config_path != ""
        config = share_dmhy_org_pb2.SHARE_DMHY_ORG_TRACKER()
        with open(config_path, "r") as f:
            json_format.Parse(f.read(), config, ignore_unknown_fields=True)
        return config
    
    @staticmethod
    async def get_rss(url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise HTTPNot200Expection
                return await response.text()
    

    def parse_xml(self, xml_data: str) -> Iterable[bangumi_pb2.Episode]:
        result_map = {}
        root = ET.fromstring(xml_data)
        # 遍历所有的item
        for item in root.findall('.//item'):
            title = item.find('title').text
            link = item.find('link').text
            pub_date = item.find('pubDate').text
            author = item.find('author').text
            enclosure = item.find('enclosure').get("url")
            enclosure = self._format_magnet(enclosure)
            
            edisode_idx = self._extra_episode_index(title)
            tags = self._collecting_tag(self._split_title(title))
            edisode: bangumi_pb2.Episode = result_map.get(edisode_idx, bangumi_pb2.Episode(index=edisode_idx))
            edisode.resources.append(
                resources_pb2.ExternalResource(
                    share_dmhy_org=resources_pb2.SHARE_DMHY_ORG(
                        magnet=resources_pb2.Magnet(
                            url=enclosure
                        ),
                        tags=tags,
                        author=author,
                        title=title,
                        page_link=link,
                        publish_timestamp=self._parse_time(pub_date),
                    )
                )
            )
            result_map[edisode_idx] = edisode
        return result_map.values()

    def _parse_time(self, time_string: str) -> int:
        format_string = "%a, %d %b %Y %H:%M:%S %z"

        # 解析时间字符串
        dt = datetime.strptime(time_string, format_string)

        # 转换为UNIX时间戳
        timestamp = dt.timestamp()
        return int(timestamp)

    @staticmethod
    def _extra_episode_index(string: str) -> str:
        pattern_1 = r"第(\d{1,3})[集话話]" # 第1集 第1话 第1話
        pattern_2 = r"-\s(\d{2,3})\s" # - 02
        pattern_3 = r"\[(\d{2,3})\]" # [03]
        pattern_4 = r"\[(\d{2,3})[vV]?\d*]" # [04v2]
        pattern_5 = r"【(\d{2,3})\】" # 【05】
        pattern_6 = r"【(\d{2,3})[vV]?\d*】" # 【06】


        for pattern in (pattern_1, pattern_2, pattern_3, pattern_4, pattern_5, pattern_6):
            match = re.search(pattern, string)
            if match:
                episode_number = match.group(1)
                if episode_number.isdecimal():
                    return episode_number
        return ""
    
    @staticmethod
    def _split_title(string: str) -> Iterable[str]:
        # 使用_、空格、【】、[]、- 和 \ 作为分隔符
        pattern = r"（|）|\(|\)|_|\s|【|】|\[|\]|-|\\"
        result = re.split(pattern, string)
        result = [x for x in result if len(x) > 0]
        return result
    
    @staticmethod
    def _collecting_tag(strings:  Iterable[str]) -> Iterable[tag_pb2.Tag]:
        result = []
        dedup = set()
        actions = [
            ShareDMHYTrackerHandler._collecting_resolution_tag,
            ShareDMHYTrackerHandler._collecting_subtitle_tag,
            ShareDMHYTrackerHandler._collecting_audio_video_fromat_tag,
            ShareDMHYTrackerHandler._collecting_bundle_tag,
            ]
        for i, s in enumerate(strings):
            # 第一个分片一般是字幕组
            if i == 0 and not s.isdigit():
                result.append(tag_pb2.Tag(tag=s))
                continue
            for action in actions:
                tag, matched = action(s)
                if matched:
                    if tag.tag not in dedup:
                        dedup.add(tag.tag)
                        result.append(tag)
                    break
        return result
    
    @staticmethod
    def _collecting_resolution_tag(string:  str) -> tuple[tag_pb2.Tag, bool]:
        # 提取分辨率
        if "1080" in string:
            return tag_pb2.Tag(tag="1080P"), True
        elif "720" in string:
            return tag_pb2.Tag(tag="720P"), True
        elif "2K" in string:
            return tag_pb2.Tag(tag="2K"), True
        elif "4K" in string:
            return tag_pb2.Tag(tag="4K"), True
        elif "2160" in string:
            return tag_pb2.Tag(tag="4K"), True
        elif "1440" in string:
            return tag_pb2.Tag(tag="2K"), True
        else:
            return tag_pb2.Tag(), False

    @staticmethod
    def _collecting_subtitle_tag(string:  str) -> tuple[tag_pb2.Tag, bool]:
        string = string.upper()
        white_list = ["字幕","内嵌", "内封", "双语", "雙語", "简", "繁", "CHT", "CHS", "BIG5","GB"]
        for s in white_list:
            if s in string:
                return tag_pb2.Tag(tag=string), True
        return tag_pb2.Tag(), False

    @staticmethod
    def _collecting_audio_video_fromat_tag(string:  str) -> tuple[tag_pb2.Tag, bool]:
        string = string.upper()
        white_list = ["MP4","MKV", "10BIT", "8BIT", "X264", "HEVC", "X265", "AAC", "AVC"]
        for s in white_list:
            if s in string:
                return tag_pb2.Tag(tag=string), True
        return tag_pb2.Tag(), False
    
    @staticmethod
    def _collecting_bundle_tag(string:  str) -> tuple[tag_pb2.Tag, bool]:
        string = string.upper()
        white_list = ["WEB","BD"]
        for s in white_list:
            if s in string:
                return tag_pb2.Tag(tag=string), True
        return tag_pb2.Tag(), False
    

    @staticmethod
    def _format_magnet(url_str: str) -> str:
        url_str = url_str[20:]
        parsed_url = urlparse("magnet://"+url_str.replace("&", "?", 1))
        query = parsed_url.query
        query_map = parse_qs(query)
        trs = query_map.get("tr", [])
        trs = trs[:min(5, len(trs))]
        query_map["tr"] = trs
        filtered_query_string = urlencode(query_map, doseq=True)
        filtered_url = urlunparse(parsed_url._replace(query=filtered_query_string))
        return filtered_url.replace("?", "&").replace("magnet://", "magnet:?xt=urn:btih:")
