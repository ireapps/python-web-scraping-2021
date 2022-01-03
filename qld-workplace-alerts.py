'''
Goal: Crawl the pages of Queensland's workplace incident alerts and save the data to CSV
'''

import time
import csv

import requests
from bs4 import BeautifulSoup


# list of headers for output CSV
headers = [
    'title',
    'link',
    'descrip',
    'date'
]

# request the page
req = requests.get("https://www.worksafe.qld.gov.au/news-and-events/alerts")

# check for HTTP errors
req.raise_for_status()

# turn the HTML into soup
soup = BeautifulSoup(req.text, 'html.parser')

# fetch a list of pagination links, then grab the last one in the list ([-1]) and access its `href` attribute
pagination = soup.find_all('a', {'class': 'pagination__link'})[-1]['href']

# get the last page number (everything after the `=` in the URL) and coerce to a number
last_page = int(pagination.split('=')[-1])

# build a range starting with 1, going to the last page of offsets, counting by 12
page_numbers = range(1, last_page+1, 12)

# open a CSV file to write to
with open('qld-workplace-alerts-data.csv', 'w') as outfile:

    # set up the writer
    writer = csv.writer(outfile)

    # write the headers
    writer.writerow(headers)

    # loop over the range of numbers you created earlier
    for number in page_numbers:

        # construct the URL to fetch
        url = f'https://www.worksafe.qld.gov.au/news-and-events/alerts?&start_rank={number}'

        # grab the page
        req = requests.get(url)

        # check for HTTP errors
        req.raise_for_status()

        # turn the HTML into soup
        soup = BeautifulSoup(req.text, 'html.parser')

        # grab a list of items on the page
        items = soup.find_all('li', {'class': 'search-results__item'})

        # loop over the list of items
        for item in items:
            hed = item.find('h4')
            title = hed.text.strip()
            link = hed.find('a')['href']
            descrip = item.find('p').text.strip()
            date = item.find('span').text.strip()

            # build a list of data to write out
            data_out = [
                title,
                link,
                descrip,
                date
            ]

            # write to file
            writer.writerow(data_out)

        print(f'Wrote data for items {number}-{number+12} ...')

        # pause for a half second
        time.sleep(0.5)
