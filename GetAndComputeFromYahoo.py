# python
# coding=utf-8
import ystockquote
import pandas as pd
import math

# print(ystockquote.get_shares_outstanding('GOOGL+AAPL'))
# print(ystockquote.get_shares_outstanding('AAPL'))
# print(ystockquote.get_float_shares('AAPL'))



symbol_list = ['0700.hk', 'BABA']


def main():
    df = initilize_data()
    print df
    get_shares_outstanding(df)


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
    df['shares_outstanding'] = map(int,shares_oustanding.encode('utf-8').split('\n'))
    df['shares_float'] = map(int,shares_float.encode('utf-8').split('\n'))
    df['price'] = map(float,shares_price.encode('utf-8').split('\n'))
    calRatio(df)
    print df





def calRatio(df):
    for index, row in df.iterrows():
        tempRatio = row['shares_float'] / row['shares_outstanding']
        final_ratio = 0
        if (tempRatio <= 15):
            final_ratio = math.ceil(tempRatio)
        elif (tempRatio <= 20):
            final_ratio = 20
        elif (tempRatio <= 30):
            final_ratio = 30
        elif (tempRatio <= 40):
            final_ratio = 40
        elif (tempRatio <= 50):
            final_ratio = 50
        elif (tempRatio <= 60):
            final_ratio = 60
        elif (tempRatio <= 70):
            final_ratio = 70
        elif (tempRatio <= 80):
            final_ratio = 80
        else:
            final_ratio = 100
        row['ratio']=final_ratio


if __name__ == "__main__":
    main()
