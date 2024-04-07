import argparse
import asyncio
import hashlib
import logging
from functools import partial
import traceback
import datetime
from config.config import Settings
from handler.tracker.share_dmhy_org_handler import ShareDMHYTrackerHandler
from handler.bangumi_handler import BangumiHandler
from proto_py.tracker.share_dmhy_org_pb2 import SHARE_DMHY_ORG_TRACKER_CONFIG
from proto_py.base import hash_pb2
from google.protobuf.timestamp_pb2 import Timestamp

def now_timestring():
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


# 配置日志输出格式和级别
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s - %(message)s')


def get_hash(data: bytes) ->  bytes:
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data)
    return sha256_hash.digest()

async def fetch_rss_data(dmhy_handler: ShareDMHYTrackerHandler,
                         bangumi_handler: BangumiHandler,
                         rss_config: SHARE_DMHY_ORG_TRACKER_CONFIG):
    try:
        rss_data = await dmhy_handler.get_rss(rss_config.rss_url)

        episodes = dmhy_handler.parse_xml(xml_data=rss_data)
        bangumi = bangumi_handler.load_bangumi_data(
            bangumi_id=rss_config.bangumi_id)
        logging.info("bangumi [%d] fetch [%d] items", rss_config.bangumi_id, len(episodes))
        bangumi = bangumi_handler.merge_bangumi_episodes(bangumi, episodes)
        bangumi = bangumi_handler.format_bangumi_data(bangumi)

        rss_data_hash = get_hash(bangumi.SerializeToString(deterministic=True))
        if rss_config.latest_resp_hash.value != rss_data_hash:
            rss_config.latest_resp_hash.CopyFrom(hash_pb2.HASH(type=hash_pb2.SHA256, value=rss_data_hash))
            rss_config.latest_update_time = now_timestring()
            logging.info("bangumi [%d: %s] do not have any updates, skipped", rss_config.bangumi_id, rss_config.key)
            return
        bangumi_handler.write_bangumi_data_file(bangumi=bangumi)
        dmhy_handler.update_config(rss_config)
    except Exception as e:
        logging.error("update bangumi [%d: %s] failed, rss key [%s], error: [%s]", rss_config.bangumi_id, rss_config.key, rss_config.key, str(e))
        traceback.print_exc()

async def main():
    parser = argparse.ArgumentParser(
    description='fetch data from share.dmhy.org and merge into databse')

    parser.add_argument('-c', '--config', help='config file', default='.env')

    args = parser.parse_args()

    config = Settings(_env_file_encoding='utf-8', _env_file=args.config)

    logging.info(config.model_dump_json(indent=4))

    dmhy_handler = ShareDMHYTrackerHandler(
        config_path=config.share_dmhy_org_tarcker_config_path)

    bangumi_handler = BangumiHandler(storage_path=config.bangumi_data_dir)

    task_fn = partial(fetch_rss_data, dmhy_handler, bangumi_handler)

    tasks = [task_fn(cfg) for cfg in dmhy_handler.rss_config.configs]

    await asyncio.gather(*tasks)

# python src/fetch_share_dmhy_org.py 
if __name__ == '__main__':
    asyncio.run(main())

    
