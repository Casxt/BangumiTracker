import pytest
from .bangumi_handler import BangumiHandler
from proto_py.bangumi.bangumi_pb2 import Episode, BangumiData
from proto_py.base.resources_pb2 import ExternalResource, Magnet, Website, SHARE_DMHY_ORG


def test_merge_bangumi_episodes(tmp_path):
    handler = BangumiHandler(str(tmp_path))
    test_bangumi = BangumiData(
        bangumi_id=1,
        episodes=[
            Episode(
                index="01",
                resources=[
                    ExternalResource(magnet=Magnet(url="magnet")),
                    ExternalResource(website=Website(url="website")),
                    ExternalResource(share_dmhy_org=SHARE_DMHY_ORG(
                        magnet=Magnet(url="share_dmhy_org"),
                    )),
                ]
            )
        ]
    )
    merge_episodes = [
        Episode(
            index="01",
            resources=[
                ExternalResource(magnet=Magnet(url="magnet")),
                ExternalResource(magnet=Magnet(url="magnet2")),
                ExternalResource(website=Website(url="website")),
                ExternalResource(website=Website(url="website2")),
                ExternalResource(share_dmhy_org=SHARE_DMHY_ORG(
                    author="author",
                    magnet=Magnet(url="share_dmhy_org"),
                )),
                ExternalResource(share_dmhy_org=SHARE_DMHY_ORG(
                    author="author2",
                    magnet=Magnet(url="share_dmhy_org2"),
                )),
            ]
        ),
        Episode(
            index="02",
            resources=[
                ExternalResource(magnet=Magnet(url="magnet")),
                ExternalResource(website=Website(url="website")),
                ExternalResource(share_dmhy_org=SHARE_DMHY_ORG(
                    magnet=Magnet(url="share_dmhy_org"),
                )),
            ]
        )
    ]
    new_bangum = handler.merge_bangumi_episodes(
        bangumi=test_bangumi, episodes=merge_episodes)
    assert len(new_bangum.episodes) == 2
    merged_episode = tuple(
        filter(lambda x: x.index == "01", new_bangum.episodes))[0]
    assert len(merged_episode.resources) == 6
    assert len(test_bangumi.episodes[0].resources) == 3

        
    website_resources = tuple(
        filter(lambda x: x.HasField("website"), merged_episode.resources))
    assert len(website_resources) == 2
    assert set([x.website.url for x in website_resources]
               ) == set(["website", "website2"])
    

    magnet_resources = tuple(
        filter(lambda x: x.HasField("magnet"), merged_episode.resources))
    assert len(magnet_resources) == 2
    assert set([x.magnet.url for x in magnet_resources]
               ) == set(["magnet", "magnet2"])

    dmhy_resources = tuple(filter(lambda x: x.HasField(
        "share_dmhy_org"), merged_episode.resources))
    assert len(dmhy_resources) == 2
    assert set([x.share_dmhy_org.magnet.url for x in dmhy_resources]
               ) == set(["share_dmhy_org", "share_dmhy_org2"])
    assert set([x.share_dmhy_org.author for x in dmhy_resources]
               ) == set(["author", "author2"])

def test_create_bangumi(tmp_path):
    handler = BangumiHandler(str(tmp_path))
    handler.create_bangumi(1, "test", "CHS", 0)
    handler.load_bangumi_index_file()
    assert len(handler.bangumi_index.index) == 1
    bangumi = handler.bangumi_index.index[0]
    assert len(bangumi.names) == 1
    name = bangumi.names[0]
    assert name.name == "test"

    handler.create_bangumi(2, "test2", "CHS", 0)
    handler.load_bangumi_index_file()
    assert len(handler.bangumi_index.index) == 2
    bangumi = handler.bangumi_index.index[1]
    assert len(bangumi.names) == 1
    name = bangumi.names[0]
    assert name.name == "test2"

    with pytest.raises(Exception):
        handler.create_bangumi(2, "test2", "CHS", 0)
    
    with pytest.raises(Exception):
        handler.create_bangumi(3, "test2", "CHS", 0)
    
    assert handler.get_bangumi_id_by_name("test2") == 2