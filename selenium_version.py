###IMPORTS###
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from mailer import Mailer as ma

import json

###EXTRACT DATA###
with open("data.json", "r") as data_file:
    data = json.load(data_file)

###DRIVER SETUP###
WINDOW_SIZE = "1920,1080"
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=%s" %WINDOW_SIZE)
options.binary_location = data["chrome_atributes"]["CHROME_PATH"]

driver = webdriver.Chrome(
                        executable_path=data["chrome_atributes"]["CHROMEDRIVER_PATH"],
                        options=options
                        )
driver.get(data["URLS"]["google_finance"])
# driver.get_screenshot_as_file("capture.png")
#print(driver.page_source)
###CODE###
# Find all stocks added to google finance
#driver.switch_to.frame(driver.find_element_by_class_name('zmhDub'))
watchlist = driver.find_element_by_id('knowledge-finance-wholepage__financial-entities-list')
print(watchlist)

# Close driver
driver.close()


