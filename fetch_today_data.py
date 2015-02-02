#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# fetch today's data
# do it everyday after market closing
#
import urllib
import json
import codecs
import re

from tool.dao_toolkit import Helper
from tool.dao_toolkit import MetastockHelper

# Exchange: SH,SZ
Market_Data_URL = 'http://quotes.money.163.com/hs/service/diyrank.php?query=STYPE:EQA;EXCHANGE:CNSE{0}&\
fields=SYMBOL,SNAME,PRICE,OPEN,HIGH,LOW,VOLUME,UPDOWN,PERCENT,TURNOVER&sort=SYMBOL&order=asc&page={1}&count={2}&type=query'


def get_market_data(exchange, page_index, page_size):
    ''' EXCHANGE - SH or SZ
    '''
    page = urllib.urlopen(Market_Data_URL.format(exchange,page_index, page_size))
    content = page.read()
    return json.loads(content)

def build_index_data_row(url, symbol, trading_day):
    page = urllib.urlopen(url)
    content = page.read()
    m = re.search(r'{"code":.*?}',content)
    # sample json data:
    #
    # {
    #   "code": "1399001",
    #   "percent": 0.006007,
    #   "high": 8773.18,
    #   "askvol3": 0,
    #   "askvol2": 0,
    #   "askvol5": 0,
    #   "askvol4": 0,
    #   "price": 8737.972,
    #   "open": 8722.425,
    #   "bid5": 0.0,
    #   "bid4": 0.0,
    #   "bid3": 0.0,
    #   "bid2": 0.0,
    #   "bid1": 0.0,
    #   "low": 8661.402,
    #   "updown": 52.179,
    #   "type": "SZ",
    #   "bidvol1": 0,
    #   "bidvol3": 0,
    #   "bidvol2": 0,
    #   "symbol": "399001",
    #   "update": "2013/10/11 15:04:13",
    #   "bidvol5": 0,
    #   "bidvol4": 0,
    #   "volume": 15098883035,
    #   "askvol1": 0,
    #   "ask5": 0.0,
    #   "ask4": 0.0,
    #   "ask1": 0.0,
    #   "name": "\u6df1\u8bc1\u6210\u6307",
    #   "ask3": 0.0,
    #   "ask2": 0.0,
    #   "arrow": "\u2191",
    #   "time": "2013/10/11 15:04:09",
    #   "yestclose": 8685.793,
    #   "turnover": 138750772201.1
    # }
    if m:
        jd = json.loads(m.group())
        row = []
        row.append(trading_day)
        row.append(symbol)
        row.append(jd["name"])
        row.append(str(jd["price"]))
        row.append(str(jd["high"]))
        row.append(str(jd["low"]))
        row.append(str(jd["open"]))
        row.append(str(jd["volume"]/100))
        row.append(str(jd["updown"]))
        row.append(str(jd["percent"]))
        row.append(str(jd["turnover"]))
        
        return ','.join(row) + '\r\n'
    else:
        return None

def get_index_data(exchange, trading_day):
    if exchange == 'SH':
        return build_index_data_row('http://api.money.126.net/data/feed/0000001,money.api', '999999', trading_day)
    elif exchange == 'SZ':
        return build_index_data_row('http://api.money.126.net/data/feed/1399001,money.api', '399001', trading_day)
    else:
        return None

def get_last_trading_day():
    page = urllib.urlopen('http://api.money.126.net/data/feed/0000001,money.api')
    content = page.read()

    m =re.search(r'(?<=\"time\": \")\d{4}/\d{2}/\d{2}', content)
    if m:
        return Helper.format_date_string(m.group(), '%Y/%m/%d', '%Y%m%d')
    else:
        return None

def extract_market_data():
    trading_day = get_last_trading_day()
    print 'fetch data @{0}'.format(trading_day)
    if trading_day:
        exchanges = ['SH', 'SZ']
        page_size = 300
        for exchange in exchanges:
            page_index = 0
            with codecs.open('output/data-{0}-{1}.txt'.format(trading_day, exchange), mode='w', encoding='gb2312') as w:
                w.write(MetastockHelper.FILE_HEADER2)
                # write the index
                w.write(get_index_data(exchange, trading_day))
                while page_index < 10:
                    json_data = get_market_data(exchange, page_index, page_size)
                    # sample json data:
                    # {
                    #   "page": 0,
                    #   "count": 1,
                    #   "order": "asc",
                    #   "total": 998,
                    #   "pagecount": 998,
                    #   "time": "2015-02-02 14:30:11",
                    #   "list": [
                    #     {
                    #       "HIGH": 14.26,
                    #       "LOW": 14.02,
                    #       "OPEN": 14.06,
                    #       "PERCENT": -0.026261,
                    #       "PRICE": 14.09,
                    #       "SNAME": "\u6d66\u53d1\u94f6\u884c",
                    #       "SYMBOL": "600000",
                    #       "TURNOVER": 2330185553,
                    #       "UPDOWN": -0.38,
                    #       "VOLUME": 164672537,
                    #       "NO": 1
                    #     }
                    #   ]
                    # }
                    if json_data and len(json_data['list']) > 0:
                        for l in json_data['list']:
                            if l['HIGH'] == 0: # ignore stock on non-trading day
                                continue
                            rows = []
                            rows.append(trading_day)
                            rows.append(l['SYMBOL'])
                            rows.append(l['SNAME'])
                            rows.append(str(l['PRICE']))
                            rows.append(str(l['HIGH']))
                            rows.append(str(l['LOW']))
                            rows.append(str(l['OPEN']))
                            rows.append(str(l['VOLUME']))
                            rows.append(str(l['UPDOWN']))
                            rows.append(str(l['PERCENT']))
                            rows.append(str(l['TURNOVER']))
                            w.write(','.join(rows) + '\r\n')
                        page_index += 1
                    else:
                        break           
            print 'done for exchange[%s], has %d pages' % (exchange, page_index)


def main():
    extract_market_data()

if __name__ == '__main__':
    main()