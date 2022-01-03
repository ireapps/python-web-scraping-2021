'''
Goal: Scrape the table of WARN notices in South Dakota into a CSV.

📚 Extra credit: Scrape data from all years into a single CSV.

'''

import csv

import requests
from bs4 import BeautifulSoup

# define a list of headers for your output CSV
headers = [
    'warn_date',
    'naics_code',
    'biz',
    'address',
    'wia_code',
    'total_employees',
    'effective_date',
    'type_code'
]

# request the page
req = requests.get('http://www.dllr.state.md.us/employment/warn.shtml')

# check for HTTP errors
req.raise_for_status()

# turn the HTML into soup
soup = BeautifulSoup(req.text, 'html.parser')

# find the table
table = soup.find('table')

# find the rows in the table
rows = table.find_all('tr')

# open a CSV file to write into
with open('warn-md-data.csv', 'w') as outfile:

    # create a writer object
    writer = csv.writer(outfile)

    # write out the headers
    writer.writerow(headers)

    # loop over the list of rows, skipping the table headers
    for row in rows[1:]:

        # find the cells in this row
        cells = row.find_all('td')

        # notice date is in the first cell
        notice_date = cells[0].text.strip()

        # naics is in the second
        naics = cells[1].text.strip()

        # company name is in the next one -- deal with leading/trailing/interior whitespace problems while you're at it
        # more details: https://stackoverflow.com/a/1546251
        company_dirty = cells[2].text.strip()
        company_clean = ' '.join(company_dirty.split())

        # same with location, which is in the
        # next cell
        location_dirty = cells[3].text.strip()
        location_clean = ' '.join(location_dirty.split())

        # WIA code is in the next one, then
        # number of employees, then effective date,
        # then type code
        wia_code = cells[4].text.strip()
        num_employees = cells[5].text.strip()
        eff_date = cells[6].text.strip()
        type_code = cells[7].text.strip()

        # build a list to write out to file
        data_out = [
            notice_date,
            naics,
            company_clean,
            location_clean,
            wia_code,
            num_employees,
            eff_date,
            type_code
        ]

        # and write the data to file
        writer.writerow(data_out)
