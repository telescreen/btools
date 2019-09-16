""" Celery Tasks to Fetch Stock price """

import logging
import time
import locale
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

from celery import shared_task
from .models import StockTimeStamp, DailyStockPrice, Company

# Get an instance of a logger
logger = logging.getLogger(__name__) # pylint: disable=invalid-name


HISTORY_BASE_URL = 'https://info.finance.yahoo.co.jp/history'

# Yahoo Finance display price of 20 days per page
ITEM_PER_PAGE = 20

# We wait for 30s before start a new company
YJ_COMFORTABLE_INTERVAL = 30

@shared_task
def daily_price_crawler():
    """ Routinely Crawl Daily StockPrice from Yahoo Finance """
    logger.info('--- Fetch Today Stock Price ---')
    today = datetime.now().strftime('%Y/%m/%d')
    crawl_all_companies(today, today)


@shared_task
def crawl_all_companies(start_date: str, end_date: str):
    """
    Crawl all stock price for all companies
    in the database from start_date to end_date
    """
    logger.info('--- Fetch data from %s to %s --', start_date, end_date)
    companies = Company.objects.all()

    sdate = datetime.strptime(start_date, '%Y/%m/%d')
    edate = datetime.strptime(end_date, '%Y/%m/%d')

    for company in companies:
        _crawl_company_stock_price(company, sdate, edate)
        time.sleep(YJ_COMFORTABLE_INTERVAL)


@shared_task
def one_time_crawl(stock_quote: str, start_date: str, end_date: str):
    """
    Crawl stock price for one company with quote as stock_quote
    in the database from start_date to end_date
    """
    logger.info('--- Fetch data for %s from %s to %s --', stock_quote, start_date, end_date)

    company = Company.objects.filter(quote=stock_quote).first()
    sdate = datetime.strptime(start_date, '%Y/%m/%d')
    edate = datetime.strptime(end_date, '%Y/%m/%d')

    if company:
        _crawl_company_stock_price(company, sdate, edate)



def _crawl_company_stock_price(company: Company, sdate: datetime, edate: datetime):
    """ Fetch one company stock price from start_date to end_date """
    requests_headers = {
        'User-Agent': 'btools/1.0',
        'From': 'ha@buihanotes.com'
    }

    days = abs((edate - sdate).days)
    weeks = _weekdiff(edate, sdate)
    number_of_pages = int(days - weeks*2) // ITEM_PER_PAGE

    for page in range(number_of_pages+1):
        request_data = {
            'code': company.quote + '.T',
            'sy': sdate.year,
            'sm': sdate.month,
            'sd': sdate.day,
            'ey': edate.year,
            'em': edate.month,
            'ed': edate.day,
            'tm': 'd',
            'p': page
        }

        request_page = requests.get(HISTORY_BASE_URL, params=request_data, headers=requests_headers)
        if request_page.status_code == 200:
            _extract_daily_stock_price(company, request_page.text)

        # Wait for 100ms before processing a new page.
        # Or YJ Finance will return error
        time.sleep(0.1)



def _extract_daily_stock_price(company: Company, data: str):
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
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    soup = BeautifulSoup(data, 'html.parser')
    table = soup.find('table', {'class': 'yjSt'})
    trs = table.find_all('tr')

    # We skip the first <tr> element as it is the header row
    for tr_tags in trs[1:]:
        tds = tr_tags.find_all('td')

        # If the number of columns is lesser than 7, it might be broken
        # or we might not need that information.
        if len(tds) < 7:
            continue

        processing_date = datetime.strptime(tds[0].text, '%Y年%m月%d日')

        sts = StockTimeStamp.objects.filter(quote=company, date=processing_date).first()
        if not sts:
            sts = StockTimeStamp(quote=company, date=processing_date, processed=False)
            sts.save()

        if not sts.processed:
            daily_price = DailyStockPrice(
                quote=company,
                date=processing_date,                       # DateTime
                open_price=locale.atof(tds[1].text),        # Opening Price
                high_price=locale.atof(tds[2].text),        # Highest Price
                low_price=locale.atof(tds[3].text),         # Lowest Price
                close_price=locale.atof(tds[4].text),       # Close Price
                volume=locale.atof(tds[5].text),            # Volume
                adjusted_price=locale.atof(tds[6].text)     # Adjusted Price
            )
            daily_price.save()

            sts.processed = True
            sts.save()


def _weekdiff(day1, day2):
    """ Return the number of weeks difference between 2 days """
    monday1 = (day1 - timedelta(days=day1.weekday()))
    monday2 = (day2 - timedelta(days=day2.weekday()))
    return abs(monday1 - monday2).days / 7
