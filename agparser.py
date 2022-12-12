"""
This file is a part of AnimeGo Monitoring Bot.

AnimeGo Monitoring Bot is a Telegram bot supposed to check the release of new episodes at <https://animego.org/>
Copyright (C) 2021 Nerovik

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import bs4
import requests


def search(title):
    request = requests.get(f"https://animego.org/search/all?q={title}")
    soup = bs4.BeautifulSoup(request.text, "html.parser")
    try:
        link = soup.find("div", class_="h5 font-weight-normal mb-2 card-title text-truncate").find("a").get('href')
        return link
    except AttributeError:
        return None
    except IndexError:
        return "-"
        
def getStatus(link):
    request = requests.get(link)
    soup = bs4.BeautifulSoup(request.text, "html.parser")
    try:
        status = soup.find_all("dd", class_="col-6 col-sm-8 mb-1")[2].text
        return status
    except AttributeError:
        return "-"
    except IndexError:
        return "-"

def getEpisodes(link):
    request = requests.get(link)
    soup = bs4.BeautifulSoup(request.text, "html.parser")
    try:
        episodes = soup.find_all("dd", class_="col-6 col-sm-8 mb-1")[1].text
        return episodes
    except AttributeError:
        return "-"
    except IndexError:
        return "-"

def getTitle(link):
    request = requests.get(link)
    soup = bs4.BeautifulSoup(request.text, "html.parser")
    try:
        title = soup.find('div', class_='anime-title').find('h1')
        return title.text
    except AttributeError:
        return "-"
    except IndexError:
        return "-"

def getThumbnail(link):
    request = requests.get(link)
    soup = bs4.BeautifulSoup(request.text, "html.parser")
    try:
        thumbnail = soup.find_all('img')[2].get('src')
        return thumbnail
    except AttributeError:
        return "-"
    except IndexError:
        return "-"

def getStudio(link):
    request = requests.get(link)
    soup = bs4.BeautifulSoup(request.text, "html.parser")
    try:
        studio = soup.find_all("dd", class_="col-6 col-sm-8 mb-1 overflow-h")[1].text
        return studio
    except AttributeError:
        return "-"
    except IndexError:
        return "-"