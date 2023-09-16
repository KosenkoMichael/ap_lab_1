import os
import requests
from bs4 import BeautifulSoup

URL = "https://www.gismeteo.ru/diary/4368/2022/1/"
page = requests.get(URL, headers={"User-Agent":"Mozilla/5.0"})
#print(page.status_code)
soup = BeautifulSoup(page.text, "html.parser")
allData =[]
filtereddata=[]
allData = soup.findAll('td', class_='first')
for data in allData:
    filtereddata.append(data.text)
print(filtereddata)