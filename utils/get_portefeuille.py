import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


driver = webdriver.Chrome()
url = "https://www.yomoni.fr/legal/supports-investissement"
r = driver.get(url)
html = driver.page_source

soup = BeautifulSoup(html, "html.parser")
rows = soup.find_all("tr")
row_list = []

for tr in rows:
    td = tr.find_all("td")
    row = [i.text for i in td]
    row_list.append(row)

df = pd.DataFrame(row_list, columns = ["Dénomination", "Type", "ISIN",'DICI'])
df.set_index('ISIN', inplace=True)
df = df.iloc[1:, 0:1]
df.to_excel('/Users/pdewilde/Documents/Projects/AG2R/assets/data.xlsx', index = True, header = True)

driver.close()