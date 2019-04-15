# -*- coding: utf-8 -*-
"""FE_recipe_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RiGkhFDZul-3bFK4k6KHmtda6P-nPuz4
"""

from urllib.request import urlopen
import bs4
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

def date_format(d):
  d = str(d).replace('-', '.')
  y = int(d.split('.')[0])
  m = int(d.split('.')[1])
  d = int(d.split('.')[2])

  date = dt.date(y, m, d)
  return date

def historical_index_naver(index_cd, page_n=1, start_date ='', end_date = '', last_page=0):
  if start_date:
    start_date = date_format(start_date)
  else:
    start_date = dt.date.today()
  if end_date:
    end_date = date_format(end_date)
  else:
    end_date = dt.date.today()
    
  naver_index = 'https://finance.naver.com/sise/sise_index_day.nhn?code=' + index_cd + '&page=' + str(page_n)
  source = urlopen(naver_index).read()
  source = bs4.BeautifulSoup(source, 'lxml')
  
  dates = source.find_all('td', class_='date')
  prices = source.find_all('td', class_='number_1')

  for n in range(len(dates)):
    this_date = dates[n].text
    this_date = date_format(this_date)
    
    if this_date <= end_date and this_date >= start_date:
      this_close = prices[n*4].text
      this_close = float(this_close)

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
    historical_index_naver(index_cd, page_n, start_date, end_date, last_page)
  
  return historical_prices

historical_prices = {}
kospi200 = historical_index_naver('KPI200', start_date='2019-01-01')

type(kospi200)

df = pd.DataFrame.from_dict(kospi200, orient='index', columns=['prices'])

plt.figure(figsize=(10,5))
plt.plot(df['prices'])
