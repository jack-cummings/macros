
from seleniumwire import webdriver  # Import from seleniumwire

# Create a new instance of the Chrome driver
# other Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)
#driver = webdriver.Chrome()

# Go to the Google home page
driver.get('https://www.harristeeter.com/weeklyad')

# Access requests via the `requests` attribute
for request in driver.requests:
    if request.response:
        if request.url.startswith(('https://dam.flippenterprise.net/flyerkit/publications/harristeeter?')):
            print(
                request.url,
                request.response.status_code,
                request.response.headers['Content-Type']
            )
