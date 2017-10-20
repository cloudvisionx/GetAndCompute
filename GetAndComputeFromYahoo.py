# python
# coding=utf-8
import ystockquote
import pandas as pd

# print(ystockquote.get_shares_outstanding('GOOGL+AAPL'))
# print(ystockquote.get_shares_outstanding('AAPL'))
# print(ystockquote.get_float_shares('AAPL'))

stock_dict = {
    'symbol': [],
    'close': [],
    'shares_outstanding': [],
    'shares_float': [],
    'shares_ratio': [],
    'weight': [],
}

symbol_list = ['0700.hk', 'BABA']


def main():
    df = initilize_data()
    print df
    get_shares_outstanding(df)


def initilize_data():
    df = pd.DataFrame(index=symbol_list,
                      columns={'close', 'shares_outstanding', 'shares_float', 'shares_ratio', 'weight'})
    # df['symbol'] = symbol_list
    return df


def get_shares_outstanding(df):
    symbol_str = ''

    for index, row in df.iterrows():
        symbol_str += index
        symbol_str += '+'
    final_symbol_str=symbol_str[0:len(symbol_str)-1]
    shares_oustanding = ystockquote.get_shares_outstanding(final_symbol_str)
    df['shares_outstanding'] = shares_oustanding.encode('utf-8').split('\n')
    print df






if __name__ == "__main__":
    main()
