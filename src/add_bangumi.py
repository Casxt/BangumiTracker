import argparse
import asyncio
import logging
from functools import partial
from config.config import Settings
from handler.tracker.share_dmhy_org_handler import ShareDMHYTrackerHandler
from handler.bangumi_handler import BangumiHandler
from proto_py.base.language_code_pb2 import LanguageCode


# 配置日志输出格式和级别
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s - %(message)s')

# python src/add_bangumi.py -i 1 -n "葬送的芙莉莲" -l CHS
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='fetch data from share.dmhy.org and merge into databse')

    parser.add_argument('-c', '--config', help='config file', default='.env')
    parser.add_argument('-i', '--id', help='bangumi id', required=True, type=int)
    parser.add_argument('-n', '--name', help='bangumi name', required=True, type=str)
    parser.add_argument('-l', '--lang', help='bangumi lang', required=True, type=str, choices=LanguageCode.keys())

    args = parser.parse_args()

    config = Settings(_env_file_encoding='utf-8', _env_file=args.config)

    logging.info(config.model_dump_json(indent=4))

    bangumi_handler = BangumiHandler(storage_path=config.bangumi_data_dir)

    bangumi_handler.create_bangumi(
        bangumi_id=args.id,
        bangumi_name=args.name,
        bangumi_name_lang=args.lang.upper(),
    )




    
