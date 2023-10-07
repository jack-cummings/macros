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
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
        # for url in urls:
        #     ts = datetime.now().strftime("%m_%d_%Y_%H_%M_%S_%f")
        #     path = f"./assets/pics_temp/{ts}.png"
        #     urllib.request.urlretrieve(url, path)
        #     img = Image.open(path)
        #     # font = ImageFont.truetype("sans-serif.ttf", 16)
        #     # # draw.text((x, y),"Sample Text",(r,g,b))
        #     # img.text((0, 0), meal, (255, 255, 255), font=font)
        #     img.save(path)
        return urls


def write_email(meals,urls):
    link1 = f'https://www.google.com/search?q={meals[0]}'.replace(' ','+')
    link2 = f'https://www.google.com/search?q={meals[1]}'.replace(' ', '+')
    link3 = f'https://www.google.com/search?q={meals[2]}'.replace(' ', '+')
    link4 = f'https://www.google.com/search?q={meals[3]}'.replace(' ', '+')
    link5 = f'https://www.google.com/search?q={meals[4]}'.replace(' ', '+')
    link6 = f'https://www.google.com/search?q={meals[5]}'.replace(' ', '+')

    # pic1 = os.listdir('./assets/pics_temp/')[0]
    # pic2 = os.listdir('./assets/pics_temp/')[1]
    # pic3 = os.listdir('./assets/pics_temp/')[2]
    # pic4 = os.listdir('./assets/pics_temp/')[3]
    # pic5 = os.listdir('./assets/pics_temp/')[4]
    # pic6 = os.listdir('./assets/pics_temp/')[5]

    pic1 = urls[0]
    pic2 = urls[1]
    pic3 = urls[2]
    pic4 = urls[3]
    pic5 = urls[4]
    pic6 = urls[5]

    meal1 = meals[0]
    meal2 = meals[1]
    meal3 = meals[2]
    meal4 = meals[3]
    meal5 = meals[4]
    meal6 = meals[5]


    email = f"""""<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <style>
       /* Add custom classes and styles that you want inlined here */
    </style>
  </head>
<body>
  <div class="bg-black">
    <div class="container">
	<h1 class="ax-center text-white text-center mb-10">Mize Meals</h1>
            <h2 class="ax-center text-white text-center mb-10">Your Meals<br>This Week</h2>
      <img class="ax-center max-w-56 mb-10 rounded-lg" src="https://images.squarespace-cdn.com/content/v1/57879a6cbebafb879f256735/1579721909133-R2KSZ8VGDGBI90DYATBK/header4.jpg">
      <p class="ax-center max-w-96 lh-lg text-white text-center text-2xl mb-10">Get inspired by the fresh flavors and cuisines of this week's meals! Completely personolized to you and the best deals at your local store.</p>
                <a class="btn btn-yellow-300 rounded-full fw-800 text-5xl py-4 ax-center mb-10 w-full w-lg-80" href="https://sites.google.com/view/mize-food/home">Visit Us</a>

    </div>
  </div>
  <div class="container">
    <div class="row">
      <div class="col-6">
        <a href="{link1}">
          <img class="max-w-48 ax-center" src="{pic1}" />
          <h5 class="ax-center text-black text-center mb-10">{meal1}</h5>
        </a>
      </div>
      <div class="col-6">
        <a href="{link2}">
          <img class="max-w-48 ax-center" src="{pic2}" />
          <h5 class="ax-center text-black text-center mb-10">{meal2}</h5>
        </a>
      </div>
    <div class="row">
      <div class="col-6">
        <a href="{link3}">
          <img class="max-w-48 ax-center" src="{pic3}" />
          <h5 class="ax-center text-black text-center mb-10">{meal3}</h5>
        </a>
      </div>
      <div class="col-6">
        <a href="{link4}">
          <img class="max-w-48 ax-center" src="{pic4}" />
          <h5 class="ax-center text-black text-center mb-10">{meal4}</h5>
        </a>
      </div>
    <div class="row">
      <div class="col-6">
        <a href="{link5}">
          <img class="max-w-48 ax-center" src="{pic5}" />
          <h5 class="ax-center text-black text-center mb-10">{meal5}</h5>
        </a>
      </div>
      <div class="col-6">
        <a href="{link6}">
          <img class="max-w-48 ax-center" src="{pic6}" />
          <h5 class="ax-center text-black text-center mb-10">{meal6}</h5>
        </a>
      </div>
    </div>
    <div class="text-muted text-center my-6">
	happy cooking- Mize <br>
    </div>
  </div>
</body>
</html>

"""
    return email

def send_email(address, html):
    email_address = "johnmcummings3@gmail.com"
    email_password = os.environ['email_code']

    # create email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"This Week's Meals"
    msg['From'] = email_address
    msg['To'] = email_address

    msg.attatch(MIMEText(html, 'html'))


    # send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)


    print('email sent')