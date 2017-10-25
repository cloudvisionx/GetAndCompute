# python
# coding=utf-8
import pandas as pd
import numpy as np
import io
import requests
import time
from datetime import datetime, timedelta
import json
import simplejson

# print(ystockquote.get_shares_outstanding('GOOGL+AAPL'))
# print(ystockquote.get_shares_outstanding('AAPL'))
# print(ystockquote.get_float_shares('AAPL'))



symbol_list = ['HKG:0400',
               'HKG:0434',
               'HKG:0700',
               'HKG:0777',
               'HKG:1060',
               'HKG:1980',
               'HKG:2280',
               'HKG:3888',
               'NASDAQ:TOUR',
               'NASDAQ:WB',
               'NASDAQ:YY',
               'NASDAQ:CYOU',
               'NASDAQ:MOMO',
               'NASDAQ:JD',
               'NASDAQ:BIDU',
               'NASDAQ:BZUN',
               'NASDAQ:CTRP',
               'NASDAQ:JOBS',
               'NASDAQ:NTES',
               'NASDAQ:SINA',
               'NASDAQ:SOHU',
               'NASDAQ:VNET',
               'TAL',
               'YRD',
               'ATHM',
               'BABA',
               'BITA',
               'CMCM',
               'JMEI',
               'LEJU',
               'SFUN',
               'VIPS',
               'WBAI',
               'WUBA']

symbol_list_v2 = ['0400',
                  '0434',
                  '0700',
                  '0777',
                  '1060',
                  '1980',
                  '2280',
                  '3888',
                  'TOUR',
                  'WB',
                  'YY',
                  'CYOU',
                  'MOMO',
                  'JD',
                  'BIDU',
                  'BZUN',
                  'CTRP',
                  'JOBS',
                  'NTES',
                  'SINA',
                  'SOHU',
                  'VNET',
                  'TAL',
                  'YRD',
                  'ATHM',
                  'BABA',
                  'BITA',
                  'CMCM',
                  'JMEI',
                  'LEJU',
                  'SFUN',
                  'VIPS',
                  'WBAI',
                  'WUBA']


def main():
    # prepare_dta()
    df=pd.read_csv('ret.csv')
    print df


def prepare_dta():
    fx = readfx()
    csii50 = readcsi50()
    df_fx = pd.DataFrame(fx['data'])
    df_csii50 = pd.DataFrame(csii50['data'])
    df_csii50['tradedate'] = df_csii50['tradedate'].map(str_csii50_to_date)
    df_fx['date'] = df_fx['date'].map(str_fx_to_date)

    df = initilize_data()
    get_fx(df, df_fx)
    get_csii50(df, df_csii50)
    df['csii50'] = df['csii50'].map(float)
    df['fx'] = df['fx'].map(float)
    # a=df.iloc[0,0]
    # df['csii50/fx'] = df.apply(lambda row: row['csii50'] / row['fx'], axis=1)
    df['csii50/fx'] = df['csii50'] / df['fx']
    get_price(df)

    fulfill_price(df)
    df.to_csv('ret.csv')
    print df


def datetime_to_date(dt):
    return dt.date()

def str_csii50_to_date(datetimestr):
    return datetime.strptime(datetimestr, "%Y-%m-%d %H:%M:%S").date()


def str_fx_to_date(datetimestr):
    return datetime.strptime(datetimestr, "%b %d, %Y").date()



def initilize_data():
    datetimes_1 = pd.date_range('2017-09-11', '2017-09-29')
    datetimes_2 = pd.date_range('2017-10-05', '2017-10-20')
    datetimes=datetimes_1.union(datetimes_2)
    dates = map(datetime_to_date, datetimes)
    columns=['csii50','fx','csii50/fx']
    columns.extend(symbol_list_v2)

    df = pd.DataFrame(index=dates,
                      columns=columns)
    # df['symbol']=symbol_list
    # df['symbol'] = symbol_list
    return df


def get_price(df):
    for symbol in symbol_list_v2:
        time.sleep(0.1)
        price = google_stocks_close_v2(symbol, 30)
        print price
        dates = price.loc[:, 'date']
        for index, row in df.iterrows():
            if index in dates.values:  # shit should be values
                record = price.loc[dates == index, :]
                # print record
                df.at[index, symbol] = record.iat[0, 1]


def get_fx(df,df_fx):
    fx_date = df_fx.loc[:,'date']
    for index, row in df.iterrows():
        if index in fx_date.values:  # shit should be values
            record = df_fx.loc[fx_date==index,:]
            # print record
            df.at[index, 'fx'] = record.iat[0, 0]

def get_csii50(df,df_csii50):
    csii50_date = df_csii50.loc[:,'tradedate']
    for index, row in df.iterrows():
        if index in csii50_date.values:  # shit should be values
            record = df_csii50.loc[csii50_date==index,:]
            # print record
            df.at[index, 'csii50'] = record.iat[0, 2]


def fulfill_price(df):
    nan_df = pd.isnull(df)
    nan_pos_array_tuple = np.where(nan_df)
    nan_index_array = nan_pos_array_tuple[0]
    nan_column_array = nan_pos_array_tuple[1]

    for index in range(len(nan_index_array)):
        df.iat[nan_index_array[index], nan_column_array[index]] = df.iat[nan_index_array[index] - 1, nan_column_array[index]]

    pass


def google_stocks(symbol, startdate=(1, 1, 2005), enddate=None):
    startdate = str(startdate[0]) + '+' + str(startdate[1]) + '+' + str(startdate[2])

    if not enddate:
        enddate = time.strftime("%m+%d+%Y")
    else:
        enddate = str(enddate[0]) + '+' + str(enddate[1]) + '+' + str(enddate[2])

    stock_url = "http://www.google.com/finance/historical?q=" + symbol + \
                "&startdate=" + startdate + "&enddate=" + enddate + "&output=csv"

    raw_response = requests.get(stock_url).content

    stock_data = pd.read_csv(io.StringIO(raw_response.decode('utf-8')))

    return stock_data


def google_stocks_close_v2(symbol, period):
    stock_url = "http://finance.google.com.hk/finance/getprices?q=" + symbol + \
                "&i=86400&p=30d&f=d,c"

    raw_response = requests.get(stock_url).content
    str_pos_TIMEZONE_OFFSET = raw_response.index('TIMEZONE_OFFSET=')
    assert str_pos_TIMEZONE_OFFSET > 0
    str_pos_begin = raw_response.index('\n', str_pos_TIMEZONE_OFFSET) + 1
    timezone_offset_str = raw_response[str_pos_TIMEZONE_OFFSET + 16:str_pos_begin - 1]
    timezone_offset_hour = int(timezone_offset_str) / 60
    new_str = raw_response[str_pos_begin:]
    pos_first_douhao = new_str.index(',')
    timestamp = new_str[1:pos_first_douhao]
    first_datetime_utc = datetime.utcfromtimestamp(float(timestamp))
    first_date_local_trader = (first_datetime_utc + timedelta(hours=timezone_offset_hour)).date()

    final_str = new_str.replace(new_str[0:pos_first_douhao], '0')
    final_str = 'ori_index,close\n' + final_str
    a = final_str.decode('utf-8')

    resp = io.StringIO(a)
    stock_data = pd.read_csv(resp)
    for index, row in stock_data.iterrows():
        ori_index = stock_data.at[index, 'ori_index']
        date = first_date_local_trader + timedelta(days=int(ori_index))
        stock_data.at[index, 'date'] = date

    return stock_data




def readfx():
    with open('reuters_fx.txt') as json_file:
        data = simplejson.load(json_file)
        return data


def readcsi50():
    with open('csii50.txt') as json_file:
        data = simplejson.load(json_file)
        return data

if __name__ == "__main__":
    main()
