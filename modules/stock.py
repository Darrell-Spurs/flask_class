
from urllib.request import urlopen
from pyquery import PyQuery as pq


def get_stock_info(sid):
    # 函數回應
    data = {
        # 是否取得資料成功
        'is_success': False,
        # 個股狀況報告
        'report': {
        }
    }
    try:
        # 爬取整個目標網頁
        page = urlopen(f'https://tw.stock.yahoo.com/q/q?s={sid}')
        # 使用big5解碼
        raw_html = page.read().decode('big5')
        # 使用PyQuery解析網站取得特定資訊
        html = pq(raw_html)
        # 使用PyQuery解析網站取得特定資訊
        # 取得條件 標籤=td 帶有屬性align=center的元素
        td_list = html('td[align=center]').text().split()
        # 名稱
        name = td_list[0]
        # 成交價
        price = td_list[3]
        # 買價
        bid = td_list[4]
        # 賣價
        offer = td_list[5]
        # 資料時間
        updated_at = td_list[2]
        report = f'個股名稱:{name} ({sid}) 成交價:{price} 買價:{bid} 賣價:{offer} 資料時間:{updated_at}'
        data['is_success'] = True
        data['report']['name'] = name
        data['report']['price'] = price
        data['report']['bid'] = bid
        data['report']['offer'] = offer
        data['report']['updated_at'] = updated_at

    except:
        data['report'] = '發生錯誤，請輸入正確的查詢個股代號'
    return data
