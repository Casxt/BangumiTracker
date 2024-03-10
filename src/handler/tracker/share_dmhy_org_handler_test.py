from .share_dmhy_org_handler import ShareDMHYTrackerHandler
    
def test__extra_episode_index():
    string = "【極影字幕·毀片黨】我們的雨色協議 第10集 BIG5 AVC 720p"
    assert ShareDMHYTrackerHandler._extra_episode_index(string) == "10"

    string = "[ANi] Bokura no Ameiro Protocol - 我們的雨色協議 - 03 [1080P][Baha][WEB-DL][AAC AVC][CHT][MP4]"
    assert ShareDMHYTrackerHandler._extra_episode_index(string) == "03"

    string = "[猎户不鸽压制] 不死不幸 / Undead Unluck [16] [1080p] [简日内嵌] [2023年10月番]"
    assert ShareDMHYTrackerHandler._extra_episode_index(string) == "16"

    string = "[爱恋字幕社][10月新番][哥布林杀手 第二季][Goblin Slayer S2][03v2][1080P][MP4][简日双语]"
    assert ShareDMHYTrackerHandler._extra_episode_index(string) == "03"
    
    string = "【幻櫻字幕組】【1月新番】【迷宮飯 Dungeon Meshi】【10】【BIG5_MP4】【1920X1080】 "
    assert ShareDMHYTrackerHandler._extra_episode_index(string) == "10"

    string = "【幻櫻字幕組】【1月新番】【迷宮飯 Dungeon Meshi】【10v3】【BIG5_MP4】【1920X1080】 "
    assert ShareDMHYTrackerHandler._extra_episode_index(string) == "10"

    string = " [GM-Team][国漫][仙逆][Renegade Immortal][2023][26][AVC][GB][1080P] "
    assert ShareDMHYTrackerHandler._extra_episode_index(string) == "26"
    
    string = "[千夏字幕组][葬送的芙莉莲_Sousou no Frieren][第23话][1080p_AVC][简体][招募新人]"
    assert ShareDMHYTrackerHandler._extra_episode_index(string) == "23"

    

    # 测试无法提取到集数的情况
    string = "【極影字幕·毀片黨】我們的雨色協議 BIG5 AVC 720p"
    assert ShareDMHYTrackerHandler._extra_episode_index(string) == ""

    
def test__split_title():
    string = "【極影字幕·毀片黨】我們的雨色協議 第10集 BIG5 (AAC_AVC 720p)"
    assert ShareDMHYTrackerHandler._split_title(string) == ['極影字幕·毀片黨', '我們的雨色協議', '第10集', 'BIG5', "AAC", 'AVC', '720p']

    # [喵萌奶茶屋&LoliHouse] 福星小子 2022年版 / Urusei Yatsura 2022 - 32 [WebRip 1080p HEVC-10bit AAC][简繁日内封字幕]


def test__collecting_tag():
    string = "[喵萌奶茶屋&LoliHouse] 福星小子 2022年版 / Urusei Yatsura 2022 - 32 [WebRip 1080p HEVC-10bit AAC][简繁日内封字幕]"
    slices = ShareDMHYTrackerHandler._split_title(string)
    tags = ShareDMHYTrackerHandler._collecting_tag(slices)
    tag_strs = [t.tag for t in tags]
    assert tag_strs == ["喵萌奶茶屋&LoliHouse", "WEBRIP", "1080P", "HEVC", "10BIT", "AAC", "简繁日内封字幕"]

def test__format_magnet():
    string = """magnet:?xt=urn:btih:VNDWLZRTWIIOD6FGZKYGR4UZI33ZQRYC&dn=&tr=http%3A%2F%2F104.143.10.186%3A8000%2Fannounce&tr=udp%3A%2F%2F104.143.10.186%3A8000%2Fannounce&tr=http%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=http%3A%2F%2Ftracker3.itzmx.com%3A6961%2Fannounce&tr=http%3A%2F%2Ftracker4.itzmx.com%3A2710%2Fannounce&tr=http%3A%2F%2Ftracker.publicbt.com%3A80%2Fannounce&tr=http%3A%2F%2Ftracker.prq.to%2Fannounce&tr=http%3A%2F%2Fopen.acgtracker.com%3A1096%2Fannounce&tr=https%3A%2F%2Ft-115.rhcloud.com%2Fonly_for_ylbud&tr=http%3A%2F%2Ftracker1.itzmx.com%3A8080%2Fannounce&tr=http%3A%2F%2Ftracker2.itzmx.com%3A6961%2Fannounce&tr=udp%3A%2F%2Ftracker1.itzmx.com%3A8080%2Fannounce&tr=udp%3A%2F%2Ftracker2.itzmx.com%3A6961%2Fannounce&tr=udp%3A%2F%2Ftracker3.itzmx.com%3A6961%2Fannounce&tr=udp%3A%2F%2Ftracker4.itzmx.com%3A2710%2Fannounce&tr=http%3A%2F%2Fopen.miotracker.com%2Fannounce&tr=http%3A%2F%2F1337.abcvg.info%2Fannounce&tr=http%3A%2F%2Fbt.okmp3.ru%3A2710%2Fannounce&tr=http%3A%2F%2Fmediaclub.tv%2Fannounce.php&tr=http%3A%2F%2Fmilanesitracker.tekcities.com%2Fannounce&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce&tr=http%3A%2F%2Fopen.acgnxtracker.com%2Fannounce&tr=http%3A%2F%2Fshare.camoe.cn%3A8080%2Fannounce&tr=http%3A%2F%2Ft.acg.rip%3A6699%2Fannounce&tr=http%3A%2F%2Ft.nyaatracker.com%2Fannounce&tr=http%3A%2F%2Ftr.cili001.com%3A8070%2Fannounce&tr=http%3A%2F%2Ftracker.files.fm%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.gbitt.info%2Fannounce&tr=http%3A%2F%2Ftracker.ipv6tracker.ru%2Fannounce&tr=http%3A%2F%2Fvps02.net.orel.ru%2Fannounce&tr=https%3A%2F%2Fcarbon-bonsai-621.appspot.com%2Fannounce&tr=https%3A%2F%2Ft.btcland.xyz%2Fannounce&tr=https%3A%2F%2Ftp.m-team.cc%2Fannounce.php&tr=https%3A%2F%2Ftr.burnabyhighstar.com%2Fannounce&tr=https%3A%2F%2Ftr.doogh.club%2Fannounce&tr=https%3A%2F%2Ftr.fuckbitcoin.xyz%2Fannounce&tr=https%3A%2F%2Ftr.highstar.shop%2Fannounce&tr=https%3A%2F%2Ftr.ready4.icu%2Fannounce&tr=https%3A%2F%2Ftracker.imgoingto.icu%2Fannounce&tr=https%3A%2F%2Ftracker.kuroy.me%2Fannounce&tr=https%3A%2F%2Ftracker.lilithraws.cf%2Fannounce&tr=https%3A%2F%2Ftracker.lilithraws.org%2Fannounce&tr=https%3A%2F%2Ftracker.nanoha.org%2Fannounce&tr=https%3A%2F%2Ftracker.tamersunion.org%2Fannounce&tr=https%3A%2F%2Ftracker.vectahosting.eu%3A8443%2Fannounce&tr=wss%3A%2F%2Ftracker.openwebtorrent.com%3A443%2Fannounce&tr=http%3A%2F%2F207.241.226.111%3A6969%2Fannounce&tr=http%3A%2F%2F207.241.231.226%3A6969%2Fannounce&tr=http%3A%2F%2F%5B2001%3A1b10%3A1000%3A8101%3A0%3A242%3Aac11%3A2%5D%3A6969%2Fannounce&tr=http%3A%2F%2F%5B2001%3A470%3A1%3A189%3A0%3A1%3A2%3A3%5D%3A6969%2Fannounce&tr=http%3A%2F%2F%5B2a04%3Aac00%3A1%3A3dd8%3A%3A1%3A2710%5D%3A2710%2Fannounce&tr=http%3A%2F%2Fbuny.uk%3A6969%2Fannounce&tr=http%3A%2F%2Ffosstorrents.com%3A6969%2Fannounce&tr=http%3A%2F%2Fhome.yxgz.vip%3A6969%2Fannounce&tr=http%3A%2F%2Fopen.tracker.ink%3A6969%2Fannounce&tr=http%3A%2F%2Fretracker.hotplug.ru%3A2710%2Fannounce&tr=http%3A%2F%2Ft.overflow.biz%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.birkenwald.de%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.bt4g.com%3A2095%2Fannounce&tr=http%3A%2F%2Ftracker.dler.org%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.mywaifu.best%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.nucozer-tracker.ml%3A2710%2Fannounce&tr=http%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=http%3A%2F%2Ftracker.skyts.net%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.zerobytes.xyz%3A1337%2Fannounce&tr=http%3A%2F%2Ffxtt.ru%2Fannounce&tr=http%3A%2F%2Fpow7.com%2Fannounce&tr=http%3A%2F%2Frt.optizone.ru%2Fannounce&tr=http%3A%2F%2Ftracker.lelux.fi%2Fannounce&tr=http%3A%2F%2Ftracker1.bt.moack.co.kr%2Fannounce&tr=http%3A%2F%2Ftracker2.dler.org%2Fannounce&tr=https%3A%2F%2Ftr.torland.ga%2Fannounce&tr=https%3A%2F%2Ftracker.foreverpirates.co%2Fannounce&tr=https%3A%2F%2Ftracker.iriseden.fr%2Fannounce&tr=https%3A%2F%2Ftracker.lelux.fi%2Fannounce&tr=https%3A%2F%2Ftracker.nitrix.me%2Fannounce&tr=https%3A%2F%2Ftracker.yarr.pt%2Fannounce&tr=http%3A%2F%2Fbtracker.top%3A11451%2Fannounce&tr=http%3A%2F%2Ftracker.openbittorrent.com%2Fannounce&tr=https%3A%2F%2F1337.abcvg.info%2Fannounce&tr=http%3A%2F%2Ftk.nvacg.org%3A3333%2Fannounce&tr=http%3A%2F%2Ftracker.loadbt.com%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.srv00.com%3A6969%2Fannounce&tr=https%3A%2F%2Ftrackme.theom.nz%2Fannounce&tr=http%3A%2F%2Fopentracker.xyz%2Fannounce&tr=http%3A%2F%2Ft.publictracker.xyz%3A6969%2Fannounce&tr=https%3A%2F%2Fchihaya-heroku.120181311.xyz%2Fannounce&tr=https%3A%2F%2Fopentracker.i2p.rocks%2Fannounce&tr=https%3A%2F%2Ftr.abiir.top%2Fannounce&tr=https%3A%2F%2Ftracker.babico.name.tr%2Fannounce&tr=ws%3A%2F%2Fhub.bugout.link%3A80%2Fannounce&tr=http%3A%2F%2Fopentracker.i2p.rocks%3A6969%2Fannounce&tr=http%3A%2F%2Ftorrenttracker.nwc.acsalaska.net%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.k.vu%3A6969%2Fannounce&tr=https%3A%2F%2Fabir0dev.github.io%2Fannounce&tr=https%3A%2F%2Fopentracker.cc%2Fannounce&tr=https%3A%2F%2Ftr.abir.ga%2Fannounce&tr=https%3A%2F%2Ftr.abirxo.cf%2Fannounce&tr=https%3A%2F%2Ftracker.feb217.tk%3A8443%2Fannounce&tr=http%3A%2F%2Fipv6.1337.cx%3A6969%2Fannounce&tr=http%3A%2F%2Fipv6.govt.hu%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.merded.xyz%3A8000%2Fannounce&tr=http%3A%2F%2F5rt.tace.ru%3A60889%2Fannounce&tr=http%3A%2F%2Fbt.3kb.xyz%2Fannounce&tr=http%3A%2F%2Fcloud.nyap2p.com%3A8080%2Fannounce&tr=http%3A%2F%2Fipv4announce.sktorrent.eu%3A6969%2Fannounce&tr=http%3A%2F%2Fp4p.arenabg.com%3A1337%2Fannounce&tr=http%3A%2F%2Frt.tace.ru%2Fannounce&tr=http%3A%2F%2Fsiambit.org%2Fannounce.php&tr=http%3A%2F%2Ftorrentsmd.com%3A8080%2Fannounce&tr=http%3A%2F%2Ftracker-cdn.moeking.me%3A2095%2Fannounce&tr=http%3A%2F%2Ftracker.dutchtracking.nl%2Fannounce&tr=http%3A%2F%2Ftracker.noobsubs.net%2Fannounce&tr=http%3A%2F%2Ftracker.trackerfix.com%2Fannounce&tr=http%3A%2F%2Ftracker.vraphim.com%3A6969%2Fannounce&tr=https%3A%2F%2Ftr.steins-gate.moe%3A2096%2Fannounce&tr=https%3A%2F%2Ftracker.coalition.space%2Fannounce&tr=https%3A%2F%2Ftracker.cyber-hub.net%2Fannounce&tr=https%3A%2F%2Ftracker.gbitt.info%2Fannounce&tr=https%3A%2F%2Ftracker.parrotsec.org%2Fannounce&tr=https%3A%2F%2Ftracker.sloppyta.co%2Fannounce&tr=https%3A%2F%2Ftracker6.lelux.fi%2Fannounce"""
    new_link = ShareDMHYTrackerHandler._format_magnet(string)
    print(new_link)
    assert new_link == "magnet:?xt=urn:btih:VNDWLZRTWIIOD6FGZKYGR4UZI33ZQRYC&tr=http%3A%2F%2F104.143.10.186%3A8000%2Fannounce&tr=udp%3A%2F%2F104.143.10.186%3A8000%2Fannounce&tr=http%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=http%3A%2F%2Ftracker3.itzmx.com%3A6961%2Fannounce&tr=http%3A%2F%2Ftracker4.itzmx.com%3A2710%2Fannounce"
