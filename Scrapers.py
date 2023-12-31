from seleniumwire import webdriver
from seleniumwire.utils import decode
import requests
import re
import pandas as pd
import json

def create_driver():
    # Create a new instance of the Chrome driver
    # Set Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def HT_Scraper(zip_code):
    """Three part HT web scrape:
    Pt. 1: Identify Store code from user-provided zipcode
    Pt. 2: Identify Product URL
    Pt. 3: Scrape Product URL"""

    'Pt. 1: Identify Store ID'
    driver = create_driver()
    driver.get(f'https://www.harristeeter.com/atlas/v1/stores/v2/locator?filter.query={zip_code}&projections=full')
    # Parse network traffic to extract access token and product url
    r = driver.requests[0].response
    body = decode(r.body, r.headers.get('Content-Encoding', 'identity'))
    store_code = [x for x in json.loads(body.decode('UTF-8'))['data']['stores'] if x['brand'] == 'HART'][0][
        'storeNumber']
    driver.close()

    'Pt. 2: Identify Product URL'
    # Load New Driver
    driver = create_driver()
    driver.get('https://www.harristeeter.com/weeklyad')

    # Parse network traffic to extract access token and product url
    for request in driver.requests:
        if request.response:
            # if request.url.startswith(('https://dam.flippenterprise.net/flyerkit/publications/harristeeter?')):
            if request.url.startswith(('https://dam.flippenterprise.net/flyerkit/publications/')):
                ref = request.url
                print(ref)

    # modify ref to user specified store
    ref = re.sub(r'store_code=.*', f'store_code={store_code}', ref)
    # define access token
    access_token = re.findall('access_token=(.*?)&', str(ref))[0]
    publication_id = requests.get(ref).json()[0]['id']
    product_url = f'https://dam.flippenterprise.net/flyerkit/publication/{publication_id}/products?display_type=all&valid_web_url=false&locale=en&access_token={access_token}'

    'Pt. 3: Scrape Products'
    products = requests.get(product_url).json()
    rdf = pd.DataFrame(products)
    df = pd.DataFrame(rdf[['id', 'name', 'sale_story', 'price_text']])
    df['is_deal'] = df['sale_story'].apply(lambda x: 1 if str(x).lower().startswith('buy') else 0)
    # df = df[df['is_deal']==1]
    foods = df['name'].to_list()
    return foods