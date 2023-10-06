import os
import openai
import gspread
import pandas as pd
import json
import re
import urllib
from PIL import Image
from PIL import ImageFont
from datetime import datetime

def pull_db():
    creds = {
      "type": os.environ['g_type'],
      "project_id": os.environ['g_proj_id'],
      "private_key_id": os.environ['g_priv_key_id'],
      "private_key": os.environ['g_priv_key'].replace('\\n', '\n'),
      "client_email": os.environ['g_client_email'],
      "client_id": os.environ['g_client_id'],
      "auth_uri": os.environ['g_auth_uri'],
      "token_uri": os.environ['g_token_uri'],
      "auth_provider_x509_cert_url": os.environ['g_auth_prov_cirt'],
      "client_x509_cert_url": os.environ['g_client_cirt_url'],
    }
    sa = gspread.service_account_from_dict(creds)
    sh = sa.open_by_key('1bVqJTqGu7rB_ED49lpq_q2YVGMiUlx7fDsSocBetZPI').sheet1
    ref_df = pd.DataFrame(sh.get_all_records())

    return ref_df

def get_meals(food):
    # prompt = f"""List the names and key ingredients of 10 dinner recipes that could be cooked using some of the
    # ingredients listed in the "food list" below and other items typically found in grocery stores. Respond with JSON
    # object of the format: {{"Recipe 1": {{"Name": "Recipe_name", "Ingredients": ["item_1", "item_2", "item_3"]}}}}.
    # Food List: {' ,'.join(food)} """
    prompt = f"""List the names  10 dinner recipes that could be cooked using some of the 
    ingredients listed in the "food list" below and other items typically found in grocery stores. Respond with a comma-seperated list of recipe names only matching the format "BEGIN meal1, meal2, meal3 meal4, meal5, meal6, meal7, meal8, meal9, meal10 END". 
    Food List: {' ,'.join(food)} """
    openai.api_key = os.environ['oaik']
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}])
    meals = completion.choices[0].message['content']
    meals = meals.replace('BEGIN','').replace('END','').split(',')
    print(meals)
    return meals

def get_pics(meals):
    for meal in meals:
        prompt = f"a {meal} plate, Sigma 85mm f/1.4, studio lighting, photorealistic. In the style of food network, high resolution"
        pics = openai.Image.create(prompt=prompt, n=1, size="256x256")
        urls = [item['url'] for item in pics['data']]
        for url in urls:
            ts = datetime.now().strftime("%m_%d_%Y_%H_%M_%S_%f")
            path = f"./assets/pics_temp/{ts}.png"
            urllib.request.urlretrieve(url, path)
            img = Image.open(path)
            # font = ImageFont.truetype("sans-serif.ttf", 16)
            # # draw.text((x, y),"Sample Text",(r,g,b))
            # img.text((0, 0), meal, (255, 255, 255), font=font)
            img.save(path)


def write_email(meals):
    base = """""<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <style>
       /* Add custom classes and styles that you want inlined here */
    </style>
  </head>
  <body class="bg-light">
    <h1 class="h1 px-1 text-gray-700"> Mesi- Your Weekly Meal Inspiration </h1>
    <div class="container">

      <!--- begin card --->
      <div class="card my-10">
        <div class="card-body bg-red-100">
          <h1 class="h3 mb-2 text-gray-700">10 Recipies for brand shoppers in {Location}</h1>
          <hr>
          <div class="space-y-3">
            <p class="text-gray-700">
              <ul>
                <li><a href="https://www.example.com/link1">{Link 1}</a></li>
                <li><a href="https://www.example.com/link2">{Link 2}</a></li>
                <li><a href="https://www.example.com/link3">{Link 3}</a></li>
                <li><a href="https://www.example.com/link4">{Link 4}</a></li>
                <li><a href="https://www.example.com/link5">{Link 5}</a></li>
                <li><a href="https://www.example.com/link6">{Link 6}</a></li>
                <li><a href="https://www.example.com/link7">{Link 7}</a></li>
                <li><a href="https://www.example.com/link8">{Link 8}</a></li>
                <li><a href="https://www.example.com/link9">{Link 9}</a></li>
                <li><a href="https://www.example.com/link10">{Link 10}</a></li>
            </ul>
            </p>
          </hr>
        </div>
        </div>
      </div>
    </div>
  </body>
</html>

""".replace('{brand}','brand').replace(
            '{location}','location').replace(
        '{link1}',meals[0])
    return base

def send_email(address):
    # TO DO: Send email
    print(address)