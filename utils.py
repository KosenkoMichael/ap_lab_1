import os
import csv 
from typing import List

import requests
from bs4 import BeautifulSoup


def parse(year_from: int, year_to: int, step: int = 1) -> List[List[str]]:
    all_data = []
    for year in range(year_from, year_to + 1, step):
        print(year)
        for month in range(1, 13):
            URL = f"https://www.gismeteo.ru/diary/4618/{year}/{month}/"
            print(f"new url is open: {year}.{month}")
            html_page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(html_page.text, "lxml")
            for day in soup.find_all("td", class_="first"):
                try:
                    temp = day.find_next()
                    press = temp.find_next()
                    wind = (
                        press.find_next_sibling()
                        .find_next_sibling()
                        .find_next_sibling()
                    )
                    night_temp = wind.find_next_sibling()
                    night_press = night_temp.find_next_sibling()
                    night_wind = (
                        night_press.find_next_sibling()
                        .find_next_sibling()
                        .find_next_sibling()
                    )
                    all_data.append(
                        [
                            day.text + "." + str(month).zfill(2) + "." + str(year),
                            "day",
                            temp.text + "°C",
                            press.text + "мм.рт.ст.",
                            wind.text,
                            "night",
                            night_temp.text + "°C",
                            night_press.text + "мм.рт.ст.",
                            night_wind.text,
                        ]
                    )
                except:
                    print(
                        "can't parse "
                        + day.text
                        + "."
                        + str(month).zfill(2)
                        + "."
                        + str(year)
                    )
    return all_data


def csv_update(data: List[List[str]]) -> None:
    path = os.path.join("test_dataset.csv")
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def main() -> None:
    csv_update(parse(2007, 2008))
    print("Загрузка завершена")
