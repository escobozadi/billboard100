# Web Data Scrapping
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import numpy as np
from datetime import date, timedelta
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def get_info(website):
    # Get data from website
    page = urlopen(website)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup


def get_songs(soup):
    songs = np.array([])

    h3 = soup.find_all("h3", id="title-of-a-story")
    s = "c-title a-no-trucate a-font-primary-bold-s"
    for i in h3:
        if s in str(i):
            # print(str(i)[-20:-1])
            start = str(i).find("\t")
            end = str(i).find("</h3>")
            song = str(i)[start+12:end]
            song = song.replace("\n", "").replace("\t", "")
            songs = np.append(songs, song)

    return songs


def get_artists(soup):
    artists = np.array([])

    span = soup.find_all("span", class_="c-label")
    s = "a-no-trucate"
    for a in span:
        if s in str(a):
            start = str(a).find("\t")
            end = str(a).find("</span>")
            artist = str(a)[start+3:end]
            artist = artist.replace("\n", "")
            artists = np.append(artists, artist)

    return artists


def get_dataset(website_link, weeks=1):
    # Building dataset with Billboard100 songs
    day = date.fromisoformat("2023-07-15")

    artists = np.array([])
    songs = np.array([])
    positions = np.array([])
    week = np.array([])
    for i in range(weeks):
        website = website_link.format(day)

        html = get_info(website)
        artists = np.append(artists, get_artists(html))
        songs = np.append(songs, get_songs(html))
        week = np.append(week, np.array([str(day)] * 100))
        positions = np.append(positions, np.arange(1, 101))

        day = day - timedelta(days=7)

    data = np.array([artists, songs, positions, week]).T
    df = pd.DataFrame(data)
    df = df.rename(columns={0: "Artists", 1: "Songs", 2: "Position", 3: "Week"})
    print(df)
    return


if __name__ == '__main__':
    website_link = "https://www.billboard.com/charts/hot-100/{}/"
    get_dataset(website_link, 4)

