import argparse
import logging
import os
from urllib.parse import urlparse

from config.config import Settings
from handler.bangumi_handler import BangumiHandler
from handler.tracker.share_dmhy_org_handler import ShareDMHYTrackerHandler

# 配置日志输出格式和级别
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s - %(message)s')

# python src/add_dmhy_rss_config.py -k "葬送的芙莉莲" -i 1 -u "https://share.dmhy.org/topics/rss/rss.xml?keyword=%E8%91%AC%E9%80%81%E7%9A%84%E8%8A%99%E8%8E%89%E8%8E%B2%7C%E8%91%AC%E9%80%81%E3%81%AE%E3%83%95%E3%83%AA%E3%83%BC%E3%83%AC%E3%83%B3"
# RSS_KEY="葬送的芙莉莲" BANGUMI_ID=1 RSS_URL="https://share.dmhy.org/topics/rss/rss.xml?keyword=%E8%91%AC%E9%80%81%E7%9A%84%E8%8A%99%E8%8E%89%E8%8E%B2%7C%E8%91%AC%E9%80%81%E3%81%AE%E3%83%95%E3%83%AA%E3%83%BC%E3%83%AC%E3%83%B3"  python src/add_dmhy_rss_config.py
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='fetch data from share.dmhy.org and merge into databse')

    parser.add_argument('-c', '--config', help='config file', default='.env')
    parser.add_argument('-k', '--key', help='rss key', required=False, type=str, default=os.environ.get('RSS_KEY'))
    parser.add_argument('-i',
                        '--bangumi_id', help='corressponding bangumi id', required=False, type=int, default=0)
    parser.add_argument('-u',
                        '--rss_url', help='rss url', required=False, type=str, default=os.environ.get('RSS_URL'))

    args = parser.parse_args()

    config = Settings(_env_file_encoding='utf-8', _env_file=args.config)

    logging.info(config.model_dump_json(indent=4))

    parsed_url = urlparse(args.rss_url)

    key = args.key.strip()
    bangumi_id = args.bangumi_id
    assert parsed_url.scheme == "https"
    assert parsed_url.hostname == "share.dmhy.org"
    assert parsed_url.path == "/topics/rss/rss.xml"
    assert len(key) > 0


    dmhy_handler = ShareDMHYTrackerHandler(
        config_path=config.share_dmhy_org_tarcker_config_path)
    
    bangumi_handler = BangumiHandler(storage_path=config.bangumi_data_dir)

    if bangumi_id == 0:
        bangumi_id = bangumi_handler.get_bangumi_id_by_name(bangumi_name=key)

    bangumi_handler.read_bangumi_data_file(bangumi_id=bangumi_id)

    new_config = dmhy_handler.add_config(key=key, bangumi_id=bangumi_id, rss_url=parsed_url.geturl())

    logging.info(new_config)
