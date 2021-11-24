from selenium.webdriver.common.by import By
import re


def getPrices(driver):
    prices = driver.find_elements(By.ID, "message-box-price")
    price = prices[0].text.strip("€")
    return price

def getPriceVar(driver):
    priceVar = driver.find_elements(By.ID, "message-box-percentage")
    priceVar = priceVar[0].text
    priceVar = re.findall("\d*\.?\d+", priceVar)
    priceVar = list(map(float, priceVar))
    return priceVar

def getDirection(driver):
    direction = driver.find_elements(By.XPATH, '//span[@data-mds-icon-name="ip-performance-arrow-down"]')
    if len(direction) > 0:
        priceTrend = "Down"
    else:
        priceTrend = "Up"
    return priceTrend

def getYield(driver):
    yieldOneYear = driver.find_elements(By.CLASS_NAME, "sal-dp-value")[7].text.strip("%")
    return yieldOneYear

    