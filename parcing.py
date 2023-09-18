from bs4 import BeautifulSoup
import csv
import os
import requests
 
def my_parser(year_from, year_to, step=1):
    parser_data = []
    for year in range(year_from, year_to + 1, step):
        for month in range(1, 13):
            URL = f"https://www.gismeteo.ru/diary/4618/{year}/{month}/"
            print(f"new url is open: {year}.{month}")
            html_page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(html_page.text, 'lxml')
            for day in soup.find_all('td', class_="first"):
                try:
                    temp = day.find_next()
                    press = temp.find_next()
                    wind = press.find_next_sibling().find_next_sibling().find_next_sibling()
                    night_temp = wind.find_next_sibling()
                    night_press = night_temp.find_next_sibling()
                    night_wind = night_press.find_next_sibling().find_next_sibling().find_next_sibling()
                    parser_data.append(["day",day.text + "." + str(month).zfill(2) + "." + str(year),
                                        temp.text + "°C", press.text + "мм.рт.ст.", wind.text,
                                        "night",night_temp.text + "°C", night_press.text + "мм.рт.ст.", night_wind.text])
                except:
                    print("Parsing error for " + day.text + "." + str(month).zfill(2) + "." + str(year))
    return parser_data

def fill_csv(parser_data):
    with open('C:\\Users\\Aspire 7\\Desktop\\Parcing\\dataset.csv', 'w', encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(parser_data)
    
fill_csv(my_parser(2008, 2023))

print("Загрузка завершена")
