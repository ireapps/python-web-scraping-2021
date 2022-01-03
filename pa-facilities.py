'''
Goal: Download the HTML behind the big list of drug and alcohol facilities in Pennsylvania.

This is step one of what would need to be a multi-part scraper to get the details, but this is the only step that needs an automated browser.
'''

from playwright.sync_api import sync_playwright

# create a playwright object in a context manager
with sync_playwright() as p:

    # create a chromium browser in non-headless mode
    browser = p.chromium.launch(headless=False)

    # open a new page
    page = browser.new_page()

    # navigate to the search page
    page.goto('https://sais.health.pa.gov/commonpoc/Content/PublicWeb/DAFind.aspx')

    # click the form submit and increase the timeout to 30 seconds
    page.click('#btnSubmit2', timeout=300000)

    # wait for the next page to appear
    page.wait_for_selector('form#frmFacInfo')

    # grab the HTML content
    html = page.content()

    # write the HTML to file
    with open('pa-facility-list.html', 'w') as outfile:
        outfile.write(html)

    # and close the browser
    browser.close()
