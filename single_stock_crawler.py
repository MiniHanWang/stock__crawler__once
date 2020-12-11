#@Time:12/10/20206:00 PM
#@Author: Mini(Wang Han)
#@Site:
#@File:single_stock.py
import requests
import pandas as pd
from datetime import datetime, time, timedelta
def get_stock_hist_Kline(code, fqt=1, start=None, end=None):
    '''
        获取个股历史日K线数据
    Parameters：
    ------
        code : string
                股票代码 e.g. 600519
        fqt: int
                复权方式, 0=不复权 1=前复权 2=后复权, 默认为1
        start: string
                开始日期 format：YYYYMMDD, 为空时为当前日期前一年的日期
        end : string
                结束日期 format：YYYYMMDD, 为空时为当前日期
    Return : dict
    ------
    '''
    if not start:
        start = datetime.strftime(datetime.now()-timedelta(days=365), "%Y%m%d")
    if not end:
        end = datetime.strftime(datetime.now(), "%Y%m%d")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    }
    params = (
        ('secid', '1.%s' % code if code[0] in ['6'] else '0.%s' % code),
        ('ut', 'fa5fd1943c7b386f172d6893dbfba10b'),
        ('fields1', 'f1,f2,f3,f4,f5'),
        ('fields2', 'f51,f52,f53,f54,f55,f56,f57,f58,f61'),
        ('klt', '101'),
        ('fqt', fqt),
        ('beg', start),
        ('end', end),
        ('_', '1585797862454'),
    )
    res = requests.get('http://72.push2his.eastmoney.com/api/qt/stock/kline/get', headers=headers, params=params, timeout=1)
    data = res.json()['data']
    return data


def clean_data_df(data):
    klines_list = [i.split(',') for i in data.get('klines')]
    df = pd.DataFrame(klines_list, columns=['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '换手'])
    df['code'] = data['code']
    df['name'] = data['name']
    return df


if __name__ == '__main__':
    codelist=[600000,600004,600006,600007,600008,600009,600010,600011,600012,600015,600016,600017,600018,600019,600020,600021,600022,600023,600025,600026]
    for code in codelist:
        try:
            data = get_stock_hist_Kline(str(code),start="20170131", end="20190131")
            if data:
                df = clean_data_df(data)
                df.to_excel(f'{code}.xlsx', index=False, encoding='gbk')
        except:
            continue
