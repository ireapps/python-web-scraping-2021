'''
Goal: scrape the list of Criterion films into a CSV.
https://www.criterion.com/shop/browse/list
'''

import csv

import requests
import bs4

# define a list of headers for the output CSV
headers = [
    'spine_no',
    'cover_img',
    'title',
    'url',
    'director',
    'country',
    'year'
]

# fetch the page
req = requests.get('https://www.criterion.com/shop/browse/list')

# turn the HTML into soup --
# note that the html5lib needs to be
# installed as a separate dependency
soup = bs4.BeautifulSoup(req.text, 'html5lib')

# target the rows in the table
rows = soup.find_all('tr', {'class': 'gridFilm'})

# open a CSV file to write out to
with open('criterion-data.csv', 'w') as outfile:

    # create a writer object
    writer = csv.writer(outfile)

    # and write the headers to file
    writer.writerow(headers)

    # loop over the rows
    for row in rows:
        # the link is actually attached to the entire row
        url = row['data-href']

        # find all the cells in this row
        cells = row.find_all('td')

        # unpack and use multiple assignment to locate the cells
        spine_no, img, title, director, country, year = cells

        # build a list of data to write out
        data_out = [
            spine_no.text.strip(),
            img.img['src'],
            title.text.strip(),
            url,
            director.text.strip(),
            country.text.strip().rstrip(','),
            year.text.strip()
        ]

        # and write this row to file
        writer.writerow(data_out)
