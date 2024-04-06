import argparse
import logging
import os

from config.config import Settings
from handler.bangumi_handler import BangumiHandler
from proto_py.base.language_code_pb2 import LanguageCode

# 配置日志输出格式和级别
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s - %(message)s')


# python src/add_bangumi.py -n "葬送的芙莉莲" -l CHS
# BANGUMI_NAME="葬送的芙莉莲" BANGUMI_NAME_LANG=CHS python src/add_bangumi.py
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='fetch data from share.dmhy.org and merge into databse')

    parser.add_argument('-c', '--config', help='config file', default='.env')
    parser.add_argument('-i', '--id', help='bangumi id', required=False, type=int)
    parser.add_argument('-n', '--name', help='bangumi name', required=False, type=str, default=os.environ.get('BANGUMI_NAME'))
    parser.add_argument('-l', '--lang', help='bangumi lang', required=False, type=str, choices=LanguageCode.keys(), default=os.environ.get('BANGUMI_NAME_LANG'))

    args = parser.parse_args()

    config = Settings(_env_file_encoding='utf-8', _env_file=args.config)

    logging.info(config.model_dump_json(indent=4))

    bangumi_handler = BangumiHandler(storage_path=config.bangumi_data_dir)

    bangumi_name: str = args.name.strip()
    bangumi_name_lang: str = args.lang.strip().upper()

    bangumi_ids = bangumi_handler.list_bangumi_ids()
    max_bangumi_id = 0 if len(bangumi_ids) == 0 else max(bangumi_ids)

    bangumi_id = args.id if args.id is not None and args.id > 0 else max_bangumi_id+1

    assert bangumi_name != ""
    assert bangumi_name_lang != ""

    bangumi = bangumi_handler.create_bangumi(
        bangumi_id=bangumi_id,
        bangumi_name=bangumi_name,
        bangumi_name_lang=args.lang.upper(),
    )

    logging.info(bangumi)




    
