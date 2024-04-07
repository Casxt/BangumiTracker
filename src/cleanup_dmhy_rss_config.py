import argparse
import logging
import os
from urllib.parse import urlparse
from config.config import Settings
from handler.bangumi_handler import BangumiHandler
from handler.tracker.share_dmhy_org_handler import ShareDMHYTrackerHandler
import datetime
# 配置日志输出格式和级别
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s - %(message)s')

# python src/cleanup_dmhy_rss_config.py -k "葬送的芙莉莲" -i 1 -u "https://share.dmhy.org/topics/rss/rss.xml?keyword=%E8%91%AC%E9%80%81%E7%9A%84%E8%8A%99%E8%8E%89%E8%8E%B2%7C%E8%91%AC%E9%80%81%E3%81%AE%E3%83%95%E3%83%AA%E3%83%BC%E3%83%AC%E3%83%B3"
# python src/cleanup_dmhy_rss_config.py
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='fetch data from share.dmhy.org and merge into databse')

    parser.add_argument('-c', '--config', help='config file', default='.env')
    parser.add_argument('-t', '--timeout_threshold_days', type=int, help='threshold of unupdated bangumi', default=30)
    args = parser.parse_args()

    config = Settings(_env_file_encoding='utf-8', _env_file=args.config)
    timeout_threshold_days = args.timeout_threshold_days
    assert timeout_threshold_days > 0
    timeout_threshold_days = datetime.timedelta(days=timeout_threshold_days)

    logging.info(config.model_dump_json(indent=4))

    dmhy_handler = ShareDMHYTrackerHandler(
        config_path=config.share_dmhy_org_tarcker_config_path)
    
    outdate_keys = []
    for config in dmhy_handler.rss_config.configs:
        if config.latest_update_time != "":
            dt = datetime.datetime.fromisoformat(config.latest_update_time).astimezone(datetime.timezone.utc)
            if (datetime.datetime.now(datetime.timezone.utc) - dt) > timeout_threshold_days:
                logging.info(f"bangumi [{config.bangumi_id}: {config.key}] not updated over {timeout_threshold_days} days, removed")
                outdate_keys.append(config.key)

    for key in outdate_keys:
        dmhy_handler.delete_config(key)

    dmhy_handler.save_config()
