# python
# coding=utf-8
import ystockquote
import pandas as pd
import math
import json
from yahoo_finance import Share

# print(ystockquote.get_shares_outstanding('GOOGL+AAPL'))
# print(ystockquote.get_shares_outstanding('AAPL'))
# print(ystockquote.get_float_shares('AAPL'))



symbol_list = ['0400.hk',
               '0434.hk',
               '0700.hk',
               '0777.hk',
               '1060.hk',
               '1980.hk',
               '2280.hk',
               '3888.hk',
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
    df = initilize_data()
    print df


def initilize_data():
    df = pd.DataFrame(index=symbol_list,
                      columns={'price', 'shares_outstanding', 'shares_float', 'ratio', 'shares_ratio', 'weight'})
    # df['symbol'] = symbol_list
    return df


def get_shares_outstanding(df):
    symbol_str = ''

    for index, row in df.iterrows():
        symbol_str += index
        symbol_str += '+'
    final_symbol_str = symbol_str[0:len(symbol_str) - 1]
    shares_oustanding = ystockquote.get_shares_outstanding(final_symbol_str)
    shares_float = ystockquote.get_float_shares(final_symbol_str)
    # shares_oustanding = ystockquote.get_bid_realtime(final_symbol_str)
    shares_price = ystockquote.get_previous_close(final_symbol_str)
    df['shares_outstanding'] = map(float, shares_oustanding.encode('utf-8').split('\n'))
    df['shares_float'] = map(float, shares_float.encode('utf-8').split('\n'))
    df['price'] = map(float, shares_price.encode('utf-8').split('\n'))
    calRatio(df)
    print df


def calRatio(df):
    for index, row in df.iterrows():
        tempRatio = (row['shares_float'] / row['shares_outstanding']) * 100
        final_ratio = 0.0
        if tempRatio <= 15.0:
            final_ratio = math.ceil(tempRatio)
        elif tempRatio <= 20.0:
            final_ratio = 20.0
        elif tempRatio <= 30.0:
            final_ratio = 30.0
        elif tempRatio <= 40.0:
            final_ratio = 40.0
        elif tempRatio <= 50.0:
            final_ratio = 50.0
        elif tempRatio <= 60.0:
            final_ratio = 60.0
        elif tempRatio <= 70.0:
            final_ratio = 70.0
        elif tempRatio <= 80.0:
            final_ratio = 80.0
        else:
            final_ratio = 100
        # row['ratio'] = final_ratio
        df.loc[index, 'ratio'] = final_ratio / 100


if __name__ == "__main__":
    main()
