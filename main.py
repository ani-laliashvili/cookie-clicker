from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import time

CHROME_DRIVER_PATH = 'C:\\...\\chromedriver'
URL = 'https://orteil.dashnet.org/cookieclicker/'

driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH))
driver.get(URL)
sleep(3)
# select language
lang = driver.find_element(By.ID, 'langSelect-EN')
lang.click()
sleep(3)
# find cookie
cookie = driver.find_element(By.ID, 'bigCookie')

product_names = driver.find_elements(By.CSS_SELECTOR, '#products .product .productName')
product_names = [product.text for product in product_names]

timeout = time.time() + 60*5
check_upgrades = time.time() + 5

limits = [1, 5, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15]

while True:
    cookie.click()

    if time.time() > check_upgrades:
        cookie_count = int(driver.find_element(By.ID, 'cookies').text.split(' ')[0].replace(',', '').replace(' million','00000').replace('.', ''))

        prices = driver.find_elements(By.CSS_SELECTOR, '#products .product .price')
        prices = [int(price.text.replace(',','').replace(' million','00000').replace('.', '')) for price in prices if price.text != '']

        owned = driver.find_elements(By.CSS_SELECTOR, '#products .product .owned')
        owned = [own_count.text for own_count in owned]

        products = driver.find_elements(By.CSS_SELECTOR, '#products .product')
        enabled = [True if product.get_attribute('class').find('toggledOff') == -1 else False for product in products]

        for x in range(len(prices)-1, -1, -1):
            #print(owned[x])
            if cookie_count > prices[x] and enabled[x] == True and (owned[x] == '' or int(owned[x]) < limits[x]):
                upgrade = driver.find_element(By.ID, f'product{x}')
                upgrade.click()
        check_upgrades = time.time() + 7

    if time.time() > timeout:
        break

cookies_per_sec = driver.find_element(By.ID, 'cookiesPerSecond')
print(cookies_per_sec.text)

driver.quit()
