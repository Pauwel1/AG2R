import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from activate import getData


excelFile = "C:/Users/pdewilde/Documents/Projects/AG2R/assets/data.xlsx"

df = pd.read_excel(excelFile)

for item in df["ISIN"]:
    url = "https://www.morningstar.com/search?query=" + item

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options = chrome_options)
    r = driver.get(url)
    html = driver.page_source
    time.sleep(10)
    singleUrl = driver.find_element(By.CLASS_NAME, "mdc-link mdc-security-module__name mds-link mds-link--no-underline").click()

    price, priceVar, direction, yieldPerYear = getData(singleUrl)
    print(price, priceVar, direction, yieldPerYear)
