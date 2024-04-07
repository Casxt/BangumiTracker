# BangumiTracker

## running locally

1. install protoc
2. execute generate_proto.sh
3. change the code
4. execute ut.sh

## script

### add new bangumi definenation

```
python src/add_bangumi.py -i 1 -n "葬送的芙莉莲" -l CHS
```

### add new rss source

```
python src/add_dmhy_rss_config.py -k "葬送的芙莉莲" -i 1 -u "https://share.dmhy.org/topics/rss/rss.xml?keyword=%E8%91%AC%E9%80%81%E7%9A%84%E8%8A%99%E8%8E%89%E8%8E%B2%7C%E8%91%AC%E9%80%81%E3%81%AE%E3%83%95%E3%83%AA%E3%83%BC%E3%83%AC%E3%83%B3"
```

### polling all rss and update database

```
python src/fetch_share_dmhy_org.py 
```
