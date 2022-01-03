'''
Goal: Scrape the table of WARN notices in South Dakota into a CSV.
'''


import csv

import requests
from bs4 import BeautifulSoup

# define a list of headers for your output CSV
headers = [
    'company',
    'city',
    'date',
    'num_workers',
    'pdf_link'
]

# fetch the page
req = requests.get('https://dlr.sd.gov/workforce_services/businesses/warn_notices.aspx')

# check for HTTP errors
req.raise_for_status()

# turn the HTML into soup
soup = BeautifulSoup(req.text, 'html.parser')

# find the table
table = soup.find('table')

# find the rows in the table
rows = table.find_all('tr')

# open a CSV file to write your data to
with open('warn-sd-data.csv', 'w') as outfile:
    
    # create a csv.writer object attached to the file handler
    writer = csv.writer(outfile)

    # write the first row into your CSV file -- the headers
    writer.writerow(headers)

    # loop over the list of rows in the table, skipping the first row of table headers
    for row in rows[1:]:

        # within this row, find all of the cells
        # (td, or table data tags)
        cells = row.find_all('td')

        # company info is in the first cell
        company_cell = cells[0]

        # the text in the tag is the name of
        # the company
        company_dirty = company_cell.text

        # deal with leading/trailing/interior whitespace problems
        # more details: https://stackoverflow.com/a/1546251
        company_clean = ' '.join(company_dirty.split())

        # some but not all of these cells contain an anchor tag linking to the PDF, so you need to use an if statement to check for that here
        if company_cell.find('a'):

            # if that anchor tag exists, grab the relative link stored in its href attribute
            # note that we also need to use lstrip() to remove the leading '/' that's present in some but not all of the links
            pdf_href = company_cell.find('a')['href'].lstrip('/')

            # and then use an f-string to build a fully qualified URL
            # https://docs.python.org/3/tutorial/inputoutput.html#tut-f-strings
            pdf_link = f'https://dlr.sd.gov/{pdf_href}'
        # or if no a tag, set the value to an empty string
        else:
            pdf_link = ''
        
        # city is in the next cell
        city = cells[1].text.strip()

        # date is in the next cell
        date = cells[2].text.strip()

        # number of employees is the last cell
        num_employees = cells[3].text.strip()

        # load the whole thing up into a list
        data_out = [
            company_clean,
            city,
            date,
            num_employees,
            pdf_link
        ]

        # and write this row of data to file
        writer.writerow(data_out)
