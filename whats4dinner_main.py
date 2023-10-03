from seleniumwire import webdriver
from seleniumwire.utils import decode
import requests
import re
import pandas as pd
import json
import os
import openai

def create_driver():
    # Create a new instance of the Chrome driver
    # Set Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def get_store_id(zip_code):
    driver = create_driver()
    driver.get(f'https://www.harristeeter.com/atlas/v1/stores/v2/locator?filter.query={zip_code}&projections=full')

    # Parse network traffic to extract access token and product url
    r = driver.requests[0].response
    body = decode(r.body, r.headers.get('Content-Encoding', 'identity'))
    store_code = [x for x in json.loads(body.decode('UTF-8'))['data']['stores'] if x['brand']=='HART'][0]['storeNumber']
    return store_code


def root_scrape(user_zip):
    # Load main HT Main
    driver = create_driver()
    driver.get('https://www.harristeeter.com/weeklyad')

    # Parse network traffic to extract access token and product url
    for request in driver.requests:
        if request.response:
            if request.url.startswith(('https://dam.flippenterprise.net/flyerkit/publications/harristeeter?')):
                ref = request.url
    # Build Product endpoint
    store_code = get_store_id(user_zip)
    # modify ref to user specified store
    ref = re.sub(r'store_code=.*', f'store_code={store_code}', ref)
    # define access token
    access_token = re.findall('access_token=(.*?)&',str(ref))[0]
    publication_id = requests.get(ref).json()[0]['id']
    product_url = f'https://dam.flippenterprise.net/flyerkit/publication/{publication_id}/products?display_type=all&valid_web_url=false&locale=en&access_token={access_token}'
    return product_url

def get_products(product_url):
    products = requests.get(product_url).json()
    rdf = pd.DataFrame(products)
    df = pd.DataFrame(rdf[['id','name','sale_story','price_text']])
    df['is_deal'] = df['sale_story'].apply(lambda x: 1 if str(x).lower().startswith('buy') else 0)
    #df = df[df['is_deal']==1]
    foods = df['name'].to_list()
    return foods

def get_meals(foods):
    prompt = f"""List the names and key ingredients of 10 dinner recipes that could be cooked using some of the ingredients
                below and other items typically found in grocery stores as json objects. {' ,'.join(food)}"""
    openai.api_key = os.environ['oaik']
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}])
    meals = completion.choices[0].message['content']
    return meals

def main(user_email,user_zip):
    product_url = root_scrape(user_zip)
    food = get_products(product_url)
    meals = get_meals(food)
    return meals





# user_zip = '27609'
# product_url1 = root_scrape(user_zip)
# food1 = get_products(product_url1)
# print(food)
#
# food == food1



# # Access requests via the `requests` attribute
# for request in driver.requests:
#     if request.response:
#         print(
#             request.url,
#             request.response.status_code,
#             request.response.headers['Content-Type']
#         )
#https://dam.flippenterprise.net/flyerkit/publications/harristeeter?locale=en&access_token=73fe8b09ea4414952d6882604003ae39&show_storefronts=true&store_code=00021