import os
import openai
import gspread
import pandas as pd
import json

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
    sh = sa.open_by_key('1WmQxtplMtfCzPb4jBjkqPvXFhdqwOpubeR5c-zBIfYs').sheet1
    ref_df = pd.DataFrame(sh.get_all_records())

    return ref_df

def get_meals(food):
    prompt = f"""List the names and key ingredients of 10 dinner recipes that could be cooked using some of the 
    ingredients listed in the "food list" below and other items typically found in grocery stores. Respond with JSON 
    object of the format: {{"Recipe 1": {{"Name": "Recipe_name", "Ingredients": ["item_1", "item_2", "item_3"]}}}}. 
    Food List: {' ,'.join(food)} """
    openai.api_key = os.environ['oaik']
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}])
    meals = completion.choices[0].message['content']
    # meals = {'Recipe 1': {'Name': 'Salmon Stir-Fry', 'Ingredients': ['Alaska Sockeye Salmon Fillets', 'Farmers Market Whole or Sliced White Mushrooms', 'Farmers Market Mini Sweet Peppers']}, 'Recipe 2': {'Name': 'Grilled Chicken Skewers', 'Ingredients': ['Marcangelo Chicken Breast Skewers', 'Farmers Market Yellow Onions', 'Farmers Market Mini Sweet Peppers']}, 'Recipe 3': {'Name': 'Chicken Parmesan', 'Ingredients': ['Marcangelo Chicken Breast Skewers', 'Harris Teeter Flour', '6-8 oz. Kraft Shredded Cheese']}, 'Recipe 4': {'Name': 'Apple Walnut Salad', 'Ingredients': ['Farmers Market Fuji Apples', 'Farmers Market Baby Spinach', 'Harris Teeter Thin Crust Pizza']}, 'Recipe 5': {'Name': 'Mushroom and Bell Pepper Omelette', 'Ingredients': ['Farmers Market Whole or Sliced White Mushrooms', 'Yellow, Orange or Red Bell Peppers', 'Harris Teeter Ultra Paper Towels']}, 'Recipe 6': {'Name': 'Cheesy Quesadillas', 'Ingredients': ['8 oz. Harris Teeter Natural Sliced Cheese', 'Tostitos or Simply', 'Harris Teeter Flour']}, 'Recipe 7': {'Name': 'Mushroom and Onion Pizza', 'Ingredients': ['Farmers Market Whole or Sliced White Mushrooms', 'Farmers Market Yellow Onions', 'Harris Teeter Ultra Paper Plates']}, 'Recipe 8': {'Name': 'Grilled Shrimp Skewers', 'Ingredients': ['Freshie Shrimp Alfredo', 'Harris Teeter Vegetable or Canola Oil', 'Farmers Market Mini Sweet Peppers']}, 'Recipe 9': {'Name': 'Pork Tenderloin with Mustard Glaze', 'Ingredients': ['Smithfield Boneless Pork Loin Filet or Tenderloin', 'Harris Teeter Flavored Mustard', 'Harris Teeter Iced Tea']}, 'Recipe 10': {'Name': 'Baked Cod with Tomato Salsa', 'Ingredients': ['Cod Fillets', "14.5 oz. Hunt's or 10 oz. Rotel Canned Tomatoes", 'Fresh Express Flat Leaf Spinach']}}
    return json.loads(meals)

def write_email(meals):
    text = f"""Looks Like Some Great Deals this Week- Your meal inspiration is:
            {meals['Recipe 1']['Name']}
            {" ,".join(meals['Recipe 1']['Ingredients'])}
            
            {" ,".join(meals['Recipe 2']['Name'])}
            {" ,".join(meals['Recipe 2']['Ingredients'])}
            
            {meals['Recipe 3']['Name']}
            {" ,".join(meals['Recipe 3']['Ingredients'])}            
            """
    return text

def send_email(address):
    # TO DO: Send email
    print(address)