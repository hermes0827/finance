# -*- coding: utf-8 -*-
"""FE_recipe_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16cFnboO9b5F0SpkmojqT2fUoF754EtUF
"""

from urllib.request import urlopen
import bs4
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import re

def date_format(d):
  d = str(d).replace('-', '.')
  y = int(d.split('.')[0])
  m = int(d.split('.')[1])
  d = int(d.split('.')[2])

  date = dt.date(y, m, d)
  return date

def historical_prices_naver(index_cd, page_n=1, start_date ='', end_date = '', last_page=0):
  if start_date:
    start_date = date_format(start_date)
  else:
    start_date = dt.date.today()
  if end_date:
    end_date = date_format(end_date)
  else:
    end_date = dt.date.today()
    
  naver_index = 'https://finance.naver.com/item/sise_day.nhn?code=' + index_cd + '&page=' + str(page_n)
  source = urlopen(naver_index).read()
  source = bs4.BeautifulSoup(source, 'lxml')
  
  dates = source.find_all('span', class_='tah p10 gray03')
  prices = source.find_all('span', class_=re.compile('^tah p11'))

  for n in range(len(dates)):
    this_date = dates[n].text
    this_date = date_format(this_date)
    
    if this_date <= end_date and this_date >= start_date:
      this_close = prices[n*6].text
      this_close = this_close.replace(",", "")
      this_close = int(this_close)

      historical_prices[this_date] = this_close
    
    elif start_date > this_date:
      return historical_prices
    
  if last_page == 0:
    last_page = source.find('td', class_='pgRR').find('a')['href']
    last_page = last_page.split('&')[1]
    last_page = last_page.split('=')[1]
    last_page = int(last_page)
      
  if page_n < last_page:
    page_n += 1
    historical_prices_naver(index_cd, page_n, start_date, end_date, last_page)
  
  return historical_prices

historical_prices = {}
historical_prices_naver('020560', start_date='2019-01-01')

