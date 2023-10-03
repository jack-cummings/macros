from Scrapers import HT_Scraper
from utils import pull_db, get_meals, send_email, write_email


def main(user_zip, brand):
    if brand == 'Harris Teeter':
        food = HT_Scraper(user_zip)
    else:
        print('dif store')
    meals = get_meals(food)
    return meals


entries = pull_db().values.tolist()
for entry in entries:
    meals = main(entry[1], entry[2])
    print(write_email(meals))
    #send_email(entry[0])


# # Access requests via the `requests` attribute
# for request in driver.requests:
#     if request.response:
#         print(
#             request.url,
#             request.response.status_code,
#             request.response.headers['Content-Type']
#         )
# https://dam.flippenterprise.net/flyerkit/publications/harristeeter?locale=en&access_token=73fe8b09ea4414952d6882604003ae39&show_storefronts=true&store_code=00021
