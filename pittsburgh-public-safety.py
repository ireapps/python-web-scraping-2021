'''
GOAL: Scrape all of the blotter items from the Pittsburgh public safety page into a CSV.

⚠️ Before running this script, first create a folder in this directory and name it pittsburgh-public-safety-pages (or whatever you like, just change the value attached to the `pages_dir` variable)

📚 Extra credit: Rewrite the downloading-pages bit so that it saves the HTML pages conditionally

'''

import time
import glob
import csv

import requests
from bs4 import BeautifulSoup

# the name of the folder where your downloaded pages will land
pages_dir = 'pittsburgh-public-safety-pages'

# list of headers to write to CSV
headers = [
    'date',
    'crime',
    'zone',
    'summary',
    'pio'
]

# request the page with the list of links
req = requests.get("https://pittsburghpa.gov/publicsafety/blotterview.html")

# check for HTTP errors
req.raise_for_status()

# turn the HTML into soup
soup = BeautifulSoup(req.text, 'html.parser')

# find the div with the links
blotlist = soup.find('div', {'id': 'blotlist'})

# pull out the list of a tags
links = blotlist.find_all('a', {'id': 'public-safety-blotter'})

# use a list comprehension to grab just the URLS
urls = [x['href'] for x in links]

# loop over the URLs, requesting each one in turn
for url in urls:

    # make the request
    req = requests.get(url)

    # grab the ID from the last part of the URL
    blotter_id = url.split('/')[-1]

    # and use it to build a file path
    filename = f'{pages_dir}/{blotter_id}.html'

    # open that new file to write into
    with open(filename, 'w') as outfile:

        # and write the HTML to file
        outfile.write(req.text)

    # let us know what you did
    print(f'Wrote {filename} to file ...')

    # pause for a half-second
    time.sleep(0.5)

# get a handle to the list of HTML files you just downloaded
local_pages = glob.glob(f'{pages_dir}/*.html')

# open a CSV file to write to
with open('pittsburgh-public-safety-data.csv', 'w') as outfile:

    writer = csv.writer(outfile)
    writer.writerow(headers)

    # loop over the list of HTML files
    for file in local_pages:

        # open the file and read in the HTML
        with open(file, 'r') as infile:
            html = infile.read()
        
        # turn the HTML into soup
        soup = BeautifulSoup(html, 'html.parser')

        # find the container div
        div = soup.find('div', {'class': 'text-style'})

        # find the H2 headline
        hed = div.find('h2').text.strip()

        # grab the span with the label/value pairs
        labels = div.find('span')

        # split on the line breaks
        label_list = str(labels).split('<br/>')

        # grab the stuff after the `</strong>` ending tag for each one
        values = [x.split('</strong>')[-1] for x in label_list]

        # date's first up, then the crime, then the zone
        date = values[0]
        crime = values[1]
        zone = values[2]

        # the HTML is kind of garbage so need to turn the summary markup back into soup, briefly, then grab the text
        summary = BeautifulSoup(values[4], 'html.parser').text

        # PIO name is last one
        pio = values[5].rstrip('</span>').strip()

        # prep a list of items to write out, stripping all extraneous whitespace while we're at it
        data_out = [
            ' '.join(date.split()),
            ' '.join(crime.split()),
            ' '.join(zone.split()),
            ' '.join(summary.split()),
            ' '.join(pio.split())
        ]

        # and write to file
        writer.writerow(data_out)
