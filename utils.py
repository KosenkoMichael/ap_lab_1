import os
import csv
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup


def parse(year_from: int, year_to: int, step: int = 1) -> List[List[str]]:
    """ open url for (year_from) to (year_to)

    Args:
        year_from (int): begin parse
        year_to (int): end_parse
        step (int, optional): step in range of years. Defaults to 1.

    Returns:
        List[List[str]]: list of rows with data {date, day: temp, press, wind_dir, wind_speed, night: temp, press, wind_dir, wind_speed}
    """
    all_data = []
    for year in range(year_from, year_to + 1, step):
        print(year)
        for month in range(1, 13):
            URL = f"https://www.gismeteo.ru/diary/4618/{year}/{month}/"
            print(f"new url is open: {year}.{month}")
            html_page = requests.get(
                URL, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(html_page.text, "lxml")
            for day in soup.find_all("td", class_="first"):
                try:
                    temp = day.find_next()
                    press = temp.find_next()
                    day_wind = (
                        press.find_next_sibling()
                        .find_next_sibling()
                        .find_next_sibling()
                    )
                    night_temp = day_wind.find_next_sibling()
                    night_press = night_temp.find_next_sibling()
                    night_wind = (
                        night_press.find_next_sibling()
                        .find_next_sibling()
                        .find_next_sibling()
                    )
                    day_wind_dirrection = ""
                    day_wind_speed = ""
                    night_wind_dirrection = ""
                    night_wind_speed = ""
                    try:
                        day_wind_dirrection = day_wind.text.split()[0]
                    except:
                        pass
                    try:
                        day_wind_speed = day_wind.text.split()[1][0]
                    except:
                        pass
                    try:
                        night_wind_dirrection = night_wind.text.split()[0]
                    except:
                        pass
                    try:
                        night_wind_speed = night_wind.text.split()[1][0]
                    except:
                        pass
                    all_data.append(
                        [
                            to_iso((day.text).zfill(2)+'-' +
                                   str(month).zfill(2)+'-' + str(year)),
                            temp.text,
                            press.text,
                            day_wind_dirrection,
                            day_wind_speed,
                            night_temp.text,
                            night_press.text,
                            night_wind_dirrection,
                            night_wind_speed
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


def csv_update(path: str, data: List[List[str]]) -> None:
    """fill csv file with data

    Args:
        path (str): path to file
        data (List[List[str]]): data, we want to write in file
    """
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def to_iso(cur_date: str) -> str:
    """return date in format "%Y-%m-%d"

    Args:
        cur_date (str): date in format "%d-%m-%Y"

    Returns:
        str: date in format "%d-%m-%Y"
    """
    date = datetime.strptime(cur_date, "%d-%m-%Y")
    return date.strftime("%Y-%m-%d")


def main() -> None:
    csv_update("dataset.csv", parse(2008, 2023))
    csv_update("test_dataset.csv", parse(2008, 2009))
    print("Загрузка завершена")
