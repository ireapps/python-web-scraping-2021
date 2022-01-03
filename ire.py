'''
Goal: Crawl the IRE News pages and scrape every item into a CSV.

Strategy: Fetch the initial page to get the total number of pages to traverse, then iterate over each page to grab the items.

📚 Extra credit: Rewrite this scraper to save the pages locally before reading them in to scrape.

📚 Extra extra credit: Same as above, but save the pages *conditionally* -- only save the ones you haven't downloaded already.

📚 Extra extra extra credit: Using the strptime() method in the datetime standard lib module, convert the post dates into YYYY-MM-DD format

'''

import csv
import time

import requests
from bs4 import BeautifulSoup


# have to spoof a browser each time, otherwise
# you get a 429 error
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0'
}

# fetch the page
req = requests.get(
    'https://www.ire.org/news/ire-news/',
    headers=headers
)

# check for HTTP problems
req.raise_for_status()

# turn the HTML into soup
soup = BeautifulSoup(req.text, 'html.parser')

# find the pagination links
pagination_links = soup.find_all(
    'a',
    {'class': 'page-numbers'}
)

# we want the second-to-last link, which has the number of the last page
# and get just the text, not the whole tag, coerced to an integer to use in the range later
last_page = int(pagination_links[-2].text)

# define a list of column headers for the CSV
csv_headers = [
    'headline',
    'link',
    'date',
    'author',
    'description',
    'tags',
]

# open a CSV file to write into
with open('ire-data.csv', 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(csv_headers)

    # loop over a range of numbers starting at 1
    # ending with the last page, plus one
    # here's some reading on why you have to add 1 to the second argument: https://stackoverflow.com/a/4504677
    for page_num in range(1, last_page+1):

        # build the URL
        url = f'https://www.ire.org/news/ire-news/page/{page_num}/'

        # fetch the page
        req = requests.get(url, headers=headers)

        # turn it into soup
        soup = BeautifulSoup(req.text, 'html.parser')

        # find the container div
        container_div = soup.find('div', {'class': 'tabular-data'})

        # find the h4 headlines in that container -- presumably more reliable than hard-coding in a bunch of CSS attributes that might change
        heds = container_div.find_all('h4')

        # loop over the heds
        for hed in heds:

            # the headline is the text inside the h4
            headline = hed.text.strip()

            # the link is contained in the nested a tag, and we just want the href attribute
            link = hed.find('a')['href']

            # move to the next sibling to grab the next two pieces of data
            date_author_div = hed.next_sibling

            # use multiple assignment as a shortcut to grab those two spans, plus a list comprehension to get the text only, not the whole tag
            date, author = [x.text.strip() for x in date_author_div.find_all(
                'span')]

            # the short description is in the next sibling
            descrip_div = date_author_div.next_sibling
            descrip = descrip_div.text.strip()

            # tags are in the next block
            # use lstrip() to remove the "Tags: " prefix
            tags = descrip_div.next_sibling.text.strip().lstrip('Tags: ')

            # build a list of data to write to CSV
            # note: the order here needs to match the order of your CSV headers
            data_out = [
                headline,
                link,
                date,
                author,
                descrip,
                tags
            ]

            # write this row of data to file
            writer.writerow(data_out)

        # Let us know this page is done
        print(f'Scraped page {page_num} ...')

        # pause for a half sec before the next request
        time.sleep(0.5)
