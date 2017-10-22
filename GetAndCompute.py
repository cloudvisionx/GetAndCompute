# python
# coding=utf-8
import json, urllib
from urllib import urlencode
import quandl


symbol_list = ['hk00400',
               'hk00434',
               'hk00700',
               'hk00777',
               'hk01060',
               'hk01980',
               'hk02280',
               'hk03888',
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



url = 'http://api.k780.com'
params_hk = {
    'app': 'finance.stock_list',
    'category': 'hk',
    'appkey': '28923',
    'sign': 'beb60597f6b5a8642fa86a51dcd1d675',
    'format': 'json',
}

params_us = {
    'app': 'finance.stock_list',
    'category': 'us',
    'appkey': '28923',
    'sign': 'beb60597f6b5a8642fa86a51dcd1d675',
    'format': 'json',
}

params_hs = {
    'app': 'finance.stock_list',
    'category': 'hs',
    'appkey': '28923',
    'sign': 'beb60597f6b5a8642fa86a51dcd1d675',
    'format': 'json',
}

params_stock_real = {
    'app': 'finance.stock_realtime',
    'appkey': '28923',
    'sign': 'beb60597f6b5a8642fa86a51dcd1d675',
    'format': 'json',
}


params_stock_history = {
  'app' : 'finance.stock_history',
    'appkey': '28923',
    'sign': 'beb60597f6b5a8642fa86a51dcd1d675',
  'format' : 'json',
}

components = {unicode('腾讯控股', "utf-8"), }
target_symbol_list = []


def main():
    data = quandl.get('GOOG/NYSE_IBM', collapse='weekly')
    data.head()
    f_hk = urllib.urlopen('%s?%s' % (url, urlencode(params_hk)))
    nowapi_call_hk = f_hk.read()
    # print content
    hk_result = json.loads(nowapi_call_hk, encoding="utf-8")
    all_stock_list = []
    if hk_result:
        if hk_result['success'] != '0':
            all_stock_list.extend(hk_result['result']['lists'])

    f_us = urllib.urlopen('%s?%s' % (url, urlencode(params_us)))
    nowapi_call_us = f_us.read()
    # print content
    us_result = json.loads(nowapi_call_us, encoding="utf-8")
    if us_result:
        if us_result['success'] != '0':
            all_stock_list.extend(us_result['result']['lists'])

    f_hs = urllib.urlopen('%s?%s' % (url, urlencode(params_hs)))
    nowapi_call_hs = f_hs.read()
    # print content
    hs_result = json.loads(nowapi_call_hs, encoding="utf-8")
    if hs_result:
        if hs_result['success'] != '0':
            all_stock_list.extend(hs_result['result']['lists'])

    for s in all_stock_list:
        if s['sname'] in components:
            print s
            target_symbol_list.append(s['symbol'].encode('utf-8'))


    # for symbol in target_symbol_list:
    #     params_stock['symbol'] = symbol
    #     print params_stock
    #     f = urllib.urlopen('%s?%s' % (url, urlencode(params_stock)))
    #     nowapi_call = f.read()
    #     a_result = json.loads(nowapi_call)
    #     if a_result:
    #         if a_result['success'] != '0':
    #             print a_result['result']
    #         else:
    #             print a_result['msgid'] + ' ' + a_result['msg']
    #     else:
    #         print 'Request nowapi fail.'
    # for symbol in symbol_list:
    #     if symbol.startswith('hk'):
    #         params_stock_real['symbol'] = symbol
    #     else:
    #         params_stock_real['symbol'] = 'gb_'+symbol.lower()
    #
    #
    #     print params_stock_real
    #     f = urllib.urlopen('%s?%s' % (url, urlencode(params_stock_real)))
    #     nowapi_call = f.read()
    #     a_result = json.loads(nowapi_call)
    #     if a_result:
    #         if a_result['success'] != '0':
    #             print a_result['result']
    #         else:
    #             print a_result['msgid'] + ' ' + a_result['msg']
    #     else:
    #         print 'Request nowapi fail.'

    params_stock_history['date'] ='20171020'
    for symbol in symbol_list:
        if symbol.startswith('hk'):
            params_stock_history['symbol'] = symbol
        else:
            params_stock_history['symbol'] = 'gb_'+symbol.lower()


        print params_stock_history
        f = urllib.urlopen('%s?%s' % (url, urlencode(params_stock_history)))
        nowapi_call = f.read()
        a_result = json.loads(nowapi_call)
        if a_result:
            if a_result['success'] != '0':
                print a_result['result']
            else:
                print a_result['msgid'] + ' ' + a_result['msg']
        else:
            print 'Request nowapi fail.'

if __name__ == "__main__":
    main()
