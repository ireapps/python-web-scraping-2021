'''
Goal: Scrape a list of lead burn instructors in Texas into a CSV.
'''


import csv

import requests
from bs4 import BeautifulSoup

# define a list of headers for your output CSV
headers = [
    'name',
    'address',
    'city',
    'state',
    'zip',
    'phone',
    'effective_date',
    'list_update_date'
]

# request the page
req = requests.get('https://www.texasagriculture.gov/Portals/0/Reports/PIR/certified_lead_burn_instructors.html')

# turn the HTML into soup
soup = BeautifulSoup(req.text, 'html.parser')

# find the element with the list update date --
# an H2 tag -- and isolate the date at the end using split()
list_update_date = soup.find('h2').text.split('AS OF')[-1].strip()

# find the correct table
table = soup.find('table', {'summary': 'CERTIFIED LEAD BURN INSTRUCTORS LIST'})

# find the rows in the table
rows = table.find_all('tr')

# open a CSV file to write into
with open('tx-lead-burn-data.csv', 'w') as outfile:
    
    # create a writer object
    writer = csv.writer(outfile)

    # write the headers into the file
    writer.writerow(headers)

    # loop over the rows, skipping the header
    for row in rows[1:]:

        # find all the cells in this row
        cells = row.find_all('td')

        # isolate each piece of data
        name = cells[1].text.strip()
        address = cells[2].text.strip()
        city = cells[3].text.strip()
        state = cells[4].text.strip()
        zipcode = cells[5].text.strip()
        phone = cells[6].text.strip()
        eff_date = cells[7].text.strip()
        
        # build a list of data to write out
        data_out = [
            name,
            address,
            city,
            state,
            zipcode,
            phone,
            eff_date,
            list_update_date
        ]

        # and write it to file
        writer.writerow(data_out)
