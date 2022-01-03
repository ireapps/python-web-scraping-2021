'''
Goal: Send a Slack alert if the Fort Calhoun Nuclear Station had a reportable event today

Before you can use this script, you'll need to
set up a Slack webhook tied to your Slack team:
https://api.slack.com/messaging/webhooks

... and then save that webhook URL as an
environment variable -- I called mine SLACK_WEBHOOK

Hit Google if you're not sure how to set an environment variable on your computer -- it will
vary depending on your OS and version -- or let
us know if you run into problems
'''

import os
import json
from datetime import date

import requests


# get today's date
today = date.today()

# grab the year
year = today.year

# get the two-digit month (zero pad to ensure)
month = str(today.month).zfill(2)

# get the two-digit day (zero pad to ensure)
day = str(today.day).zfill(2)

# construct the url
url = f'https://www.nrc.gov/reading-rm/doc-collections/event-status/event/{year}/{year}{mmonth}{day}en.html'

# the text to look for on the page
text_to_search = 'fort calhoun'

# fetch the page and check for HTTP errors 
req = requests.get(url)
req.raise_for_status()

# if this text appears in the HTML anywhere
# (casefold text down to ensure a match)
if text_to_search in req.text.casefold():

    # get the slack webhook URL from your
    # computer's environment
    slack_hook = os.environ.get('SLACK_WEBHOOK')

    # build a payload dictionary to deliver to the
    # Slack webhook URL, with details on how and where the message should appear
    # https://api.slack.com/reference/messaging/payload
    payload = {
        'channel': '#fcs-alerts',
        'username': 'FCS Alerter Bot',
        'icon_emoji': ':warning:',
        'text': f'I found a new reportable event for FCS: {url}'
    }

    # dump it to a JSON string
    payload_as_json = json.dumps(payload)

    # doublecheck that you have the slack webhook environment variable -- if so, use requests to post that data to the webhook url
    if slack_hook:
        requests.post(
            slack_hook,
            data=payload_as_json
        )
    # if not, let us know we need it
    else:
        print('You need the "SLACK_WEBHOOK" environment variable.')
