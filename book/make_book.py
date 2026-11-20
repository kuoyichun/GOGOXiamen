"""產生 A6 旅遊書（可彩色印刷、騎馬釘裝訂）。

用法（在 repo 根目錄）：
    python3 book/make_book.py
會產生 book/book.html 和 book/xiamen-guidebook-a6.pdf。
行程時間、地址、美食是從 assets/data.js 讀的；景點的小故事寫在下面的 STORY。
"""
import html, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_HTML = os.path.join(ROOT, 'book', 'book.html')
OUT_PDF = os.path.join(ROOT, 'book', 'xiamen-guidebook-a6.pdf')


def load_trip():
    js = "global.window={};require(process.argv[1]);process.stdout.write(JSON.stringify(window.TRIP))"
    return json.loads(subprocess.check_output(['node', '-e', js, os.path.join(ROOT, 'assets', 'data.js')]))


T = load_trip()
P = T['places']
DAYS = {d['id']: d for d in T['days']}
ITEMS = {it['id']: it for d in T['days'] for it in d['items'] if it.get('id')}
e = html.escape

# ---------------------------------------------------------------- 文字內容
# 每個景點：title 標題、img 照片、lead 介紹、story 小故事、tip 小知識、place 地址（給司機看）
STORY = {
    'ship': dict(
        day='d1', t='14:00', title='坐船到廈門：小三通', img='ferry',
        lead='從金門水頭碼頭坐船到廈門五通碼頭，大約 30 分鐘。天氣好的時候，在船上就看得到廈門的高樓。',
        story='2001 年 1 月 2 日，兩艘金門的客輪「太武號」和「浯江號」，載著大約 180 位金門鄉親開到廈門，這是兩岸隔了五十多年後，第一次有客船直接往來。以前要去大陸，得先繞到香港或日本。到現在，坐小三通往來金廈的旅客已經超過兩千四百萬人次。'),
    'zs': dict(
        day='d1', t='17:00', title='中山路步行街', img='zhongshan', place='zsroad',
        lead='飯店就在旁邊。整條街是行人徒步區，兩邊是騎樓老房子，有很多小吃和伴手禮店，晚上燈亮起來特別漂亮。',
        story='中山路大約在 1925 年開始興建，全長約 1.2 公里，從海邊的輪渡碼頭一路往東。兩旁的騎樓，多半是 1920 年代從南洋回鄉的華僑蓋的，樓上住人、樓下開店，下雨天也淋不到雨，跟台灣的老街很像。現在被評為「中國歷史文化名街」。'),
    'peanut': dict(
        day='d2', t='07:30', title='早餐：黃則和花生湯', img='breakfast', place='peanut',
        lead='中山路上的老店，從 1945 年開到現在。花生湯是甜湯，花生煮到入口即化，也可以在附近吃廈門人早餐常吃的麵線糊。'),
    'bashi': dict(
        day='d2', t='08:30', title='八市逛早市', img=None, place='bashi',
        lead='八市就是「第八市場」，從飯店走路約 10 分鐘。早上海鮮剛送到，是一天最熱鬧的時候。可以看活海鮮、看在地人買菜，也可以買芒果乾當伴手禮，想吃什麼就買一點小吃。',
        story='聽老一輩的廈門人說，八市大約在 1920、30 年代就形成了。因為離輪渡碼頭近，漁船一靠岸，海鮮就直接送來賣，一直是廈門最新鮮的海鮮集散地。八市其實是兩個市場合起來的：裡面的營平市場和外面的開禾市場，兩旁也都是騎樓。'),
    'npt': dict(
        day='d2', t='10:15', title='南普陀寺', img='nanputuo', place='npt', book=True,
        lead='坐車約 15 分鐘。千年閩南古寺，香火很旺，可以進去拜拜。寺廟依山而建，一路往上走，可以看到廟宇建築和後面的五老峰山景。',
        story='南普陀寺始建於唐末五代，最早叫「泗洲院」，宋朝改稱「無盡岩」，明朝又叫「普照寺」。清朝康熙年間重修，加蓋了供奉觀音菩薩的大悲殿。浙江的普陀山是有名的觀音道場，這座寺在它的南邊，所以叫「南普陀」。'),
    'veg': dict(split=True, 
        day='d2', t='11:30', title='南普陀素菜館', img=None, place='nptveg', book=True,
        lead='就在寺裡，是廈門很有名的素菜館。一樓是自助餐，樓上可以點菜。',
        tip='這裡的素菜做得很講究，菜名也很雅緻，像「半月沉江」「南海金蓮」，光看名字就很有意思。'),
    'ear': dict(split=True, 
        day='d2', t='15:45', title='悅享採耳', img='caier', place='ear', book=True,
        lead='從飯店走路約 5 分鐘。請師傅用小工具清耳朵，躺著大約一個小時，很舒服，常常有人做到一半就睡著。不想做的人可以在附近逛逛。',
        tip='採耳是很傳統的手藝，在四川最有名，現在很多城市都有。'),
    'xcx': dict(
        day='d2', t='17:00', title='小埕戲・海景晚餐', img='gulangyu-dusk', place='xcx', book=True,
        lead='在和平碼頭 4 樓，閩南古厝的裝潢，靠窗就正對鼓浪嶼。傍晚去剛好看夕陽，天黑後鼓浪嶼的燈一盞盞亮起來。招牌菜有紅蟳米糕、薑母鴨。',
        story='這個碼頭很有故事：2001 年第一班小三通的船，就是從金門開到這個和平碼頭靠岸。我們第一天坐的小三通，就是從那一天開始的。'),
    'pier': dict(
        day='d3', t='08:15', title='廈鼓碼頭', img='pier', place='xiagu', book='船票要事先訂',
        lead='在國際郵輪中心裡面。每個人都要用自己的台胞證換上船的憑證，台胞證記得帶在身上。坐船到鼓浪嶼大約 15 分鐘。'),
    'gly': dict(
        day='d3', t='09:45', title='鼓浪嶼', img='gulangyu', place='gly',
        lead='島上沒有汽車，到處是一百年前的老洋房、小巷和海邊步道。最適合散步，看建築、看海景，放慢腳步輕鬆逛。島上也有電瓶車可以坐。',
        story='島的西南邊海灘上，有一塊兩公尺多高、中間有洞的礁石，漲潮時海浪打進洞裡，聲音像打鼓一樣，叫做「鼓浪石」，島也在明朝時因此改名「鼓浪嶼」，在那之前叫「五龍嶼」。'),
    'gly2': dict(
        day='d3', title='鼓浪嶼的萬國建築', img='gulangyu-view',
        story='清朝末年，很多國家的領事館、商人和傳教士住進鼓浪嶼，蓋了各式各樣的洋樓、教堂和學校，所以有「萬國建築博覽」的稱號。島上的鋼琴也特別多，還有一座鋼琴博物館，被叫做「鋼琴之島」。2017 年，鼓浪嶼以「歷史國際社區」被列為世界文化遺產。'),
    'spa': dict(split=True, 
        day='d3', t='15:00', title='泰印象主題 SPA', img='massage', place='foot', book=True,
        lead='跟飯店在同一條路上，在 2 樓。做足療加全身按摩，大約 80 分鐘，躺在包廂裡還可以看電影。',
        tip='按得太大力，就跟師傅說「輕一點」。有人推銷辦卡，就說「我們是遊客，不辦卡，謝謝」。'),
    'tea': dict(split=True, 
        day='d3', t='16:40', title='不只有茶', img=None, place='tea', book=True,
        lead='海景茶館，大窗戶正對鼓浪嶼，還有鋼琴演奏。一邊喝功夫茶，一邊看夕陽，廈門 12 月大約五點半天黑。',
        tip='功夫茶是閩南人的日常：用小茶壺、小茶杯，一泡一泡慢慢喝。常喝的是烏龍茶，有名的鐵觀音就產在福建安溪。'),
    'zhcity': dict(
        day='d3', t='17:45', title='中華城逛逛・吃晚餐', img='zhcity', place='zhcity',
        lead='從茶館走過來約 10 分鐘，回飯店也很近。閩南風格的老街，有小吃和文創小店，看到想吃的就進去吃晚餐。'),
    'spw': dict(
        day='d4', t='09:45', title='沙坡尾', img='shapowei', place='spw',
        lead='以前的老漁港，漁船還停在港邊，兩邊是彩色的老房子、咖啡店和文創小店。這裡是散步看風景的地方，看到喜歡的咖啡店就進去坐坐。',
        story='這一帶以前叫「玉沙坡」，是廈門最早的漁港。1920 年代廈門沿著海邊築堤蓋馬路，原本的小漁港被填掉，漁船就搬到沙坡尾，蓋了新的避風塢，颱風天可以躲進來。後來漁業慢慢沒落，老工廠、老倉庫改成藝術區和咖啡店，就是現在的「沙坡尾藝術西區」。'),
    'yixi': dict(split=True, 
        day='d4', t='11:30', title='雙子塔・一席海景午餐', img='shimao', place='yixi', book=True,
        lead='從沙坡尾走路約 5 分鐘。中午在 5 樓的一席吃海景午餐，窗外就是海和演武大橋。',
        tip='世茂海峽大廈是兩棟像船帆的高樓，大約 300 公尺高，2015 年完工，大家都叫它「雙子塔」，是廈門很醒目的地標。'),
    'yj': dict(
        day='d4', t='13:30', title='嶼見閩南', img='yujian', place='yujian', book='門票要事先訂',
        lead='坐車約 30 分鐘。全部在室內，有冷氣，像走進一座閩南古城，表演一場接一場。',
        story='2025 年 5 月才開幕。裡面分成宋朝、海上絲路、市井煙火、南洋四個時空，每天有將近 30 場表演：大型實景演出《千年回響》、提線木偶、飛天表演，還有《鼓浪風雲》大戲。'),
    'yj2': dict(
        day='d4', title='看表演小提醒', img=None,
        lead='表演全部都已經付過了。只有換古裝、做手工、買吃的，才要另外付錢。晚餐就在館內的小吃街吃。',
        tip='提線木偶是泉州的傳統戲，一尊木偶身上有十幾條到三十幾條線，全靠師傅的手指操控，動作細膩得像真人一樣。'),
    'pack': dict(split=True, 
        day='d4', t='18:00', title='回飯店・收行李', img='souvenir', place='hotel',
        lead='回飯店前，在中山路買最後的伴手禮。隔天要早起坐船，晚上先把行李收好。',
        tip='肉乾、香腸這些肉做的東西不能帶回台灣。小三通的行李重量有限制，伴手禮不要買太重。'),
    'back': dict(
        day='d5', t='08:45', title='坐船回金門', img='wutong', place='wutong',
        lead='退房後坐車約 40 分鐘到五通碼頭，辦報到、出境，坐船約 30 分鐘回到金門水頭碼頭（船班時間以領隊通知為準）。'),
    'km': dict(
        day='d5', t='10:30', title='包計程車逛金門', img='kinmen',
        lead='在水頭碼頭坐上包車，行李放車上，由司機帶路逛金門。照片是金門的地標莒光樓，1952 年建成。'),
    'mofan': dict(
        day='d5', t='12:00', title='金城模範街', img='jincheng', place='mofan',
        lead='中午在金城的模範街吃午餐、買貢糖。',
        story='整條街是紅磚拱廊的老店屋，1924 年開始興建、1925 年完成，由當時的商會會長傅錫琪發起。他希望這條街成為以後建設的「模範」，所以叫模範街。'),
    'gongtang': dict(
        day='d5', title='金門貢糖的故事', img=None,
        story='金門貢糖是用花生和麥芽糖做的，口感酥鬆。其實貢糖最早來自廈門，後來在金門發揚光大；1959 年在全國商品展得到最優等，從此成為金門最有名的伴手禮。這趟從廈門玩到金門，剛好把貢糖的故事走了一圈。'),
    'home': dict(
        day='d5', t='17:40', title='飛回台北松山', img='kinmen-airport-2',
        lead='15:45 到金門機場報到，17:40 起飛，回到台北松山機場。旅途愉快，辛苦了！'),
}

# 每天的頁面順序
ORDER = {
    'd1': ['ship', 'zs'],
    'd2': ['peanut', 'bashi', 'npt', 'veg', 'ear', 'xcx'],
    'd3': ['pier', 'gly', 'gly2', 'spa', 'tea', 'zhcity'],
    'd4': ['spw', 'yixi', 'yj', 'yj2', 'pack'],
    'd5': ['back', 'km', 'mofan', 'gongtang', 'home'],
}
# 給司機看的地址卡（要坐車才會到的地方）
DRIVER = ['npt', 'xcx', 'xiagu', 'spw', 'yixi', 'yujian', 'wutong']

WORDS = [('計程車', '出租車・打車'), ('捷運', '地鐵'), ('廁所', '衛生間'), ('塑膠袋', '塑料袋'),
         ('冷氣', '空調'), ('鳳梨', '菠蘿'), ('番茄', '西紅柿'), ('馬鈴薯', '土豆'), ('影片', '視頻')]


# ---------------------------------------------------------------- 版面
def img(name, cls='ph'):
    return '<img class="%s" src="../img/%s.webp" alt="">' % (cls, name) if name else ''


def tag(book):
    if not book:
        return ''
    return '<span class="tag">%s</span>' % e(book if isinstance(book, str) else '要事先訂')


def addr_box(key):
    pl = P[key]
    return ('<div class="addr"><div class="addr-k">地址（給司機看）</div><div class="addr-n" lang="zh-Hans">%s</div>'
            '<div class="addr-a" lang="%s">%s</div></div>') % (e(pl['sc']), 'zh-Hant' if pl.get('tw') else 'zh-Hans', e(pl['addr']))


pages = []


def page(body, cls='', color=None, tab=None):
    pages.append((body, cls, color, tab))


def spot_pages(key, color, tab):
    s = STORY[key]
    head = ''
    if s.get('t'):
        head += '<div class="time">%s %s</div>' % (e(s['t']), tag(s.get('book')))
    head += '<h2>%s</h2>' % e(s['title'])
    first = img(s['img']) if s.get('img') else ''
    first += head
    if s.get('lead'):
        first += '<p class="lead">%s</p>' % e(s['lead'])
    rest = ''
    if s.get('story'):
        rest += '<div class="story"><span class="story-k">小故事</span><p>%s</p></div>' % e(s['story'])
    if s.get('tip'):
        rest += '<div class="story tip"><span class="story-k">小知識</span><p>%s</p></div>' % e(s['tip'])
    if s.get('place'):
        rest += addr_box(s['place'])
    # 一個景點：第一頁放照片和介紹，第二頁放小故事和地址（內容少就合成一頁）
    if not (s.get('story') and s.get('lead')) and not (s.get('split') and s.get('img')):
        page(first + rest, 'spot', color, tab)
    else:
        page(first, 'spot', color, tab)
        if rest:
            page('<div class="cont">%s</div>' % e(s['title']) + rest, 'spot', color, tab)


# 封面
page('<div class="cv-ph">%s</div><div class="cv-t"><div class="cv-k">2026 冬天・五天四夜</div><h1>廈門</h1>'
     '<div class="cv-d">12/16（三）— 12/20（日）</div><div class="cv-s">金門・廈門・鼓浪嶼</div></div>' % img('gulangyu-dusk', 'cv-img'),
     'cover')

# 怎麼用＋聯絡
page('<h2>這本書怎麼用</h2><ul class="list">'
     '<li>每天一個顏色，跟手機網頁一樣。</li>'
     '<li>每個景點都有照片、介紹和「小故事」。</li>'
     '<li>要坐車時，翻到最後面的<b>「給司機看」</b>地址卡。</li>'
     '<li>封底是飯店地址，迷路時給人看。</li></ul>'
     '<h3>聯絡電話</h3><div class="fill"><span>領隊</span></div><div class="fill"><span>同行</span></div>'
     '<div class="fill"><span>同行</span></div><div class="fill"><span>飯店</span></div>', 'info')

# 飯店
page(img('hotel') + '<div class="time">四晚都住這裡</div><h2>壺香悅</h2><p class="lead">中山路步行街店。紅白色的洋樓，門口是圓拱玻璃門，就在中山路步行街旁邊。</p>'
     + addr_box('hotel'), 'spot')

# 五天總覽
def overview(ids):
    h = ''
    for did in ids:
        d = DAYS[did]
        n = int(did[1:])
        h += '<div class="ov" style="--c:%s"><div class="ov-h"><b>第 %d 天</b> %d/%d（%s）</div><div class="ov-t">%s</div></div>' % (
            d['color'], n, T['month'], d['d'], d['wk'], e(d['title']))
    return h

page('<h2>五天行程總覽</h2>' + overview(['d1', 'd2', 'd3', 'd4', 'd5']), 'info')

# 出發前
page('<h2>天氣和穿著</h2><p class="lead">12 月的廈門，白天大約 15 到 20 度，早晚 10 到 13 度左右，跟台北的冬天差不多。</p>'
     '<ul class="list"><li>海邊風大，感覺會比較冷，帶一件防風外套。</li><li>12 月很少下雨，早上偶爾有霧。</li>'
     '<li>穿一雙好走的鞋子，散步逛街都舒服。</li></ul>', 'info')
page('<h2>出發前小叮嚀</h2><ul class="list"><li><b>台胞證</b>每天帶在身上，坐船去鼓浪嶼要用。</li>'
     '<li>付錢由領隊處理，每個人也帶一點人民幣現金。</li><li>手機開漫遊，LINE 才能用。</li>'
     '<li>肉乾、香腸這些肉做的東西不能帶回台灣。</li><li>小三通的行李重量有限制，伴手禮不要買太重。</li></ul>', 'info')

# 每一天
for did in ['d1', 'd2', 'd3', 'd4', 'd5']:
    d = DAYS[did]
    n = int(did[1:])
    rows = ''.join('<li><b>%s</b><span>%s</span></li>' % (e(it['t']), e(it.get('nb') if it['kind'] == 'move' else it['title']))
                   for it in d['items'] if it.get('t'))
    page('<div class="day-hd"><div class="seal"><small>第</small>%d<small>天</small></div><div><div class="dd">%d/%d（%s）</div>'
         '<div class="dt">%s</div></div></div><ul class="tl">%s</ul>' % (n, T['month'], d['d'], d['wk'], e(d['title']), rows),
         'dayp', d['color'], n)
    for key in ORDER[did]:
        spot_pages(key, d['color'], n)

# 廈門必吃
page('<div class="sect"><div class="sect-k">吃的</div><h1>廈門必吃</h1><p>十道廈門的道地味道，看到就點來吃吃看。</p></div>', 'sectp', '#B23A26')
for f in T['foods']:
    pl = f.get('at')
    pl = P[pl] if isinstance(pl, str) else pl
    body = (img(f['img']) if f.get('img') else '<div class="ph ph-none"><span>%s</span></div>' % e(f['name']))
    body += '<h2>%s</h2><div class="what">%s</div><ul class="list">%s</ul>' % (
        e(f['name']), e(f['what']), ''.join('<li>%s</li>' % e(p) for p in f['pts']))
    if pl:
        body += '<div class="where"><span>想吃可以去</span>%s</div>' % e(pl['n'])
    page(body, 'spot food', '#B23A26', 'eat')

# 台灣說法 vs 廈門說法
page('<h2>台灣說法・廈門說法</h2><table class="words">%s</table><p class="note">廈門人也講閩南話，跟台語很像，可以說說看！</p>'
     % ''.join('<tr><td>%s</td><td>→</td><td>%s</td></tr>' % (e(a), e(b)) for a, b in WORDS), 'info')

# 給司機看
page('<div class="sect"><div class="sect-k">坐車用</div><h1>給司機看</h1><p>要坐車時，翻到要去的地方，把這頁給司機看。</p></div>', 'sectp', '#2B1A12')
for key in DRIVER:
    pl = P[key]
    cut = pl['sc'].find('（')
    name = e(pl['sc'][:cut]) + '<small>%s</small>' % e(pl['sc'][cut:]) if cut > 0 else e(pl['sc'])
    page('<div class="drv-k">%s</div><div class="drv" lang="zh-Hans"><p class="drv-p">请送我到这里，谢谢</p><p class="drv-n">%s</p><p class="drv-a">%s</p></div>'
         % (e(pl['n']), name, e(pl['addr'])), 'driver')

# 補到 4 的倍數（筆記頁），最後一頁是封底
while (len(pages) + 1) % 4:
    page('<h2>筆記</h2>' + '<div class="line"></div>' * 11, 'info')
hp = P['hotel']
page('<div class="bk-in"><div class="bk-k">迷路的時候，請把這頁給人看</div><div class="drv" lang="zh-Hans"><p class="drv-p">请送我到这里，谢谢</p>'
     '<p class="drv-n">壶香悦<small>（厦门中山路步行街店）</small></p><p class="drv-a">%s</p></div></div>' % e(hp['addr']), 'back')

# ---------------------------------------------------------------- 輸出
CSS = open(os.path.join(ROOT, 'book', 'book.css')).read()
out = []
for i, (body, cls, color, tab) in enumerate(pages, 1):
    side = 'odd' if i % 2 else 'even'
    style = (' style="--c:%s"' % color) if color else ''
    tabh = ''
    if tab:
        k = 6 if tab == 'eat' else tab
        tabh = '<div class="tab" style="top:%.1fmm">%s</div>' % (12 + (k - 1) * 15, '吃' if tab == 'eat' else tab)
    num = '' if cls in ('cover', 'back') else '<div class="no">%d</div>' % i
    out.append('<section class="pg %s %s"%s>%s%s%s</section>' % (cls, side, style, body, tabh, num))
doc = ('<!DOCTYPE html><html lang="zh-Hant-TW"><head><meta charset="utf-8"><title>廈門旅遊書</title>'
       '<style>%s</style></head><body>%s</body></html>') % (CSS, '\n'.join(out))
open(OUT_HTML, 'w').write(doc)
print('pages:', len(pages))

# 用 Chromium 印成 PDF，並檢查有沒有字擠出頁面
js = r"""
const { chromium } = require('playwright');
(async () => {
  const [html, pdf] = process.argv.slice(1);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + html, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(800);
  const over = await p.evaluate(() => [...document.querySelectorAll('.pg')].map((s, i) => s.scrollHeight > s.clientHeight + 1 ? (i + 1) + ':' + (s.scrollHeight - s.clientHeight) : null).filter(Boolean));
  console.log('overflow pages:', over.join(' ') || 'none');
  await p.pdf({ path: pdf, width: '105mm', height: '148mm', printBackground: true });
  await b.close();
})();
"""
subprocess.run(['node', '-e', js, OUT_HTML, OUT_PDF], check=True)
print('pdf:', OUT_PDF)
