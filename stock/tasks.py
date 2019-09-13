# Celery Tasks to Fetch Stock price

import logging
import time
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from celery import shared_task
from .models import StockTimeStamp, DailyStockPrice, Company

# Get an instance of a logger
logger = logging.getLogger(__name__)


BASE_URL = 'https://info.finance.yahoo.co.jp/history'

# Yahoo Finance display price of 20 days per page
ITEM_PER_PAGE = 20

@shared_task
def DailyPriceCrawler():
    """ Routinely Crawl Daily StockPrice from Yahoo Finance """
    logger.info('--- Start to fetch new feed ---')


@shared_task
def OneTimeCrawl(stock_quote, start_date, end_date):
    logger.info('--- Fetch data for {} from {} to {} --'.format(stock_quote, start_date, end_date))

    sdate = datetime.strptime(start_date, '%Y/%m/%d')
    edate = datetime.strptime(end_date, '%Y/%m/%d')

    days = abs((edate - sdate).days)
    weeks = _weekdiff(edate, sdate)
    number_of_pages = int(days - weeks*2) // ITEM_PER_PAGE
    for page in range(number_of_pages+1):
        request_data = {
            'code': stock_quote + '.T',
            'sy': sdate.year,
            'sm': sdate.month,
            'sd': sdate.day,
            'sy': sdate.year,
            'sm': sdate.month,
            'sd': sdate.day,
            'p': page
        }
        r = requests.get(BASE_URL, params=request_data)
        if r.status_code == 200:
            print(_extractDailyStockPrice(stock_quote, r.text))


def _extractDailyStockPrice(stock_quote, data):
    """ Extract table using BeautifulSoup
    Return: an DailyStockPrice object with information extract from table
    Colume 1: DateTime
    Colume 2: Opening Price
    Colume 3: Highest Price
    Colume 4: Lowest Price
    Colume 5: Closing Price
    Colume 6: Volume
    Colume 7: Adjusted Price (For example after Stock Split)
    """
    soup = BeautifulSoup(data, 'html.parser')
    table = soup.find('table', {'class': 'yjSt'})
    trs = table.find_all('tr')

    # We skip the first <tr> element as it is the header row
    for tr in trs[1:]:
        tds = tr.find_all('td')
        sts = StockTimeStamp(stock_quote, datetime.strptime(tds[0].text, '%Y年%m月%d日'))
        sts.save()

        print(DailyStockPrice(quote=sts.quote,
                date=sts.date,    # DateTime
                open_price=tds[1].text,    # Opening Price
                high_price=tds[2].text,    # Highest Price
                low_price=tds[3].text,    # Lowest Price
                close_price=tds[4].text,    # Close Price
                volume=tds[5].text,    # Volume
                adjusted_price=tds[6].text     # Adjusted Price
            ))


def _weekdiff(day1, day2):
    monday1 = (day1 - timedelta(days=day1.weekday()))
    monday2 = (day2 - timedelta(days=day2.weekday()))
    return (abs(monday1 - monday2).days / 7)