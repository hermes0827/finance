
# coding: utf-8

# In[350]:


import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import json


# In[351]:


def agg_value(index_cd):
    url = 'https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd='+ str(index_cd)
    data = requests.get(url)
    soup = BeautifulSoup(data.content, 'html.parser')
    
    agg = soup.select('#cTB11 > tbody > tr > td')[4].contents
    floating_stocks = soup.select('#cTB11 > tbody > tr > td')[6].contents
    
    agg = re.sub('\s', '', agg[0])
    floating_stocks = re.sub('\s', '', floating_stocks[0])
    
    agg = float(agg.split('억원')[0].replace(',', ''))
    floating_stock = float(floating_stocks.split('/')[1].replace('%', ''))
    floating_ratio = floating_stocks.split('/')[0].replace('주', '')
    floating_ratio = float(floating_ratio.replace(',', ''))
    
    return agg, floating_stock, floating_ratio


# In[392]:


def top_10():
    url = 'https://finance.daum.net/api/trend/market_capitalization?page=1&perPage=30&fieldName=marketCap&order=desc&market=KOSPI&pagination=true'
    headers = {
    'accept' : 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding' : 'gzip, deflate, br',
    'accept-language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie' : 'webid=a52a85960039415fb97a245576cb34fc; _ga=GA1.2.1347221116.1555650225; _gid=GA1.2.1151933618.1555650225; TIARA=lBb2Ougu_XR5QQ3GlYDnUOstbhDCn8mx34mICN5rBcrsfXqC..R3F-6njG1Oxw3SVNyAhG4zohq-s5mhUanb7OmPmifye5_p; webid_sync=1555650225850; _gat_gtag_UA_128578811_1=1; _dfs=MWF5KzJWR3RhbFFzbXN4Ylg5UG02Q1piYjNoVVFPb1l1K0hhUEZMeGJHd3gwSDQxNGNQTW1kdmpsQ0IvOWEza1F4QkpreVFwbXdDd2d4L0JmTnlvM3c9PS0tVUFzL01rYlJUd0dLUE8vcTkwWjhoQT09--2c81036331fa9fd9e39403beab3e33f9441dd170',
    'if-none-match' : 'W/"9a47bd61cb0de633ca41189fb802c90f"',
    'referer' : 'https://finance.daum.net/domestic/market_cap',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'x-requested-with' : 'XMLHttpRequest',
    }
    data = requests.get(url, headers=headers)
    data = json.loads(data.text)['data']
    
    top_10 = {}
    
    for i in range(10):
        rank = data[i]['rank']
        name = data[i]['name']
        code = data[i]['symbolCode'][1:]
        price = data[i]['tradePrice']
        agg = data[i]['marketCap']
        
        top_10[rank] = [name, code, price, agg]
        
    return top_10

