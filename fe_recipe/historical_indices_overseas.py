
# coding: utf-8

# In[90]:


import requests
from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
import json
import datetime as dt


# In[91]:


def date_format(d):
  d = str(d).replace('-', '.')
  y = int(d.split('.')[0])
  m = int(d.split('.')[1])
  d = int(d.split('.')[2])

  date = dt.date(y, m, d)
  return date


# In[130]:


def historical_index_daum(index_cd, page_n=1, start_date='', end_date='',last_page=0):
    if start_date:
        start_date = date_format(start_date)
    else:
        start_date = dt.date.today()
    if end_date:
        end_date = date_format(end_date)
    else:
        end_date = dt.date.today()
    
    daum_url = 'http://finance.daum.net/api/quote/'+index_cd+'/days?symbolCode='+index_cd+'&page='+str(page_n)+'&perPage=10&pagination=true'
    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding' : 'gzip, deflate',
    'Accept-Language' : 'en-US,en;q=0.9,ko;q=0.8,it;q=0.7',
    'Connection' : 'keep-alive',
    'Cookie' : 'webid=2ea353f937bd4a3cb941247cf2652d6a; webid_sync=1522888398111; _ga=GA1.3.2105244674.1523919070; _ga=GA1.2.2105244674.1523919070; _gid=GA1.2.877762057.1555508799; TIARA=uEnmTstYxqwKbKm_6vXkUlsZtOfKkC9tL-Rg457wNvlupxTnN4fd4bo4ValTrmWxU8yX.R.Md1_3LWbajH-hqufaL9S5HcvJ; _dfs=TktmY0NqcUpRWVhpQlloTmdJZXVYRGtSQ2psT2RKOE12bWN5YVpWaXRJNUdJS1c1cWJjWXVjSzNnQ0w1WkpwQUsweFRMdXkxL3c5WDdLMVZkNXdDc0E9PS0tOHp4NEREVnRWWGpxTTFhR3pIYjFOQT09--e4db43e483026c88918c754c26dfe56ad1609bac',
    'Host': 'finance.daum.net',
    'If-None-Match' : 'W/"fe4f355ae19744bbc1e270f1ee6aed95"',
    'Referer' : 'http://finance.daum.net/global/quotes/US.SP500',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'X-Requested-With' : 'XMLHttpRequest'
    }
    source = requests.get(daum_url, headers = headers)
    data = json.loads(source.text)
    
    for d in data['data']:
        this_date = dt.datetime.strptime(d['date'], '%Y-%m-%d %H:%M:%S')
        this_date = dt.datetime.date(this_date)
        
        if this_date <= end_date and this_date >= start_date:
            this_close = d['tradePrice']
            data_collection[this_date] = this_close
        elif start_date > this_date:
            return data_collection
        
    if last_page == 0:
        last_page = data['totalPages']
      
    if page_n < last_page:
        page_n += 1
        historical_index_daum(index_cd, page_n, start_date, end_date, last_page)


# In[134]:


data_collection = {}
historical_index_daum('US.SP500', start_date='2019-01-01')


# In[135]:


data_collection

