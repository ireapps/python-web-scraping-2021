'''
Goal: Scrape a list of journalists accredited to cover the U.S. Congress and write to a CSV.

📚 Extra credit: Scrape the list of affiliations and links into a dictionary, with the names of the outlet as keys and their URLs as values, then use that dictionary to look up each affiliation as you process the member rows and add a new column at the end, the outlet's web address
'''

import csv

import requests
from bs4 import BeautifulSoup

# define the list of headers for CSV
headers = [
    'first',
    'last',
    'affiliation'
]

# make the request
req = requests.get('https://www.dailypress.senate.gov/membership/membership-lists/')

# turn the HTML into soup
soup = BeautifulSoup(req.text, 'html.parser')

# find the table
table = soup.find('table')

# grab a list of table rows
rows = table.find_all('tr')

# open a CSV file to write to
with open('press-gallery-data.csv', 'w') as outfile:

    # create a writer object
    writer = csv.writer(outfile)

    # write the list of headers to file
    writer.writerow(headers)

    # loop over the rows, skipping the header
    for row in rows[1:]:

        # find the cells in this row
        cells = row.find_all('td')

        # grab first/last/affil and save
        # some typing by unpacking and
        # using a list comp w/ a conditional
        first, last, affil = [x.text.strip() for x in cells if x.text]

        # write data to file
        writer.writerow([first, last, affil])
