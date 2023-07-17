# Web Data Scrapping
from bs4 import BeautifulSoup
from datetime import date, timedelta
from urllib.request import urlopen
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class Dataset(object):

    def __init__(self, website_link, weeks=1, start_day="2023-07-15"):
        self.website = website_link
        self.weeks = weeks
        self.date = start_day
        self.day = date.fromisoformat(self.date)
        self.name = "billboard100_{}_{}.csv".format(self.date,
                                                    str(self.day - timedelta(days=7*self.weeks)))
        dataset = self.get_dataset()
        dataset.to_csv("./" + self.name)

    def get_dataset(self):
        # Building dataset with Billboard100 songs
        # day = date.fromisoformat(self.date)

        artists = np.array([])
        songs = np.array([])
        positions = np.array([])
        week = np.array([])
        for i in range(self.weeks):
            website_link = self.website.format(self.day)

            html = self.get_info(website_link)
            artists = np.append(artists, self.get_artists(html))
            songs = np.append(songs, self.get_songs(html))
            week = np.append(week, np.array([str(self.day)] * 100))
            positions = np.append(positions, np.arange(1, 101))

            self.day = self.day - timedelta(days=7)

        data = np.array([artists, songs, positions, week]).T
        df = pd.DataFrame(data)
        df = df.rename(columns={0: "Artists", 1: "Songs", 2: "Position", 3: "Week"})
        return df

    @staticmethod
    def get_info(link):
        # Get data from website
        page = urlopen(link)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        return soup

    @staticmethod
    def get_songs(soup):
        songs = np.array([])

        h3 = soup.find_all("h3", id="title-of-a-story")
        s = "c-title a-no-trucate a-font-primary-bold-s"
        for i in h3:
            if s in str(i):
                start = str(i).find("\t")
                end = str(i).find("</h3>")
                song = str(i)[start+12:end]
                song = song.replace("\n", "").replace("\t", "")
                songs = np.append(songs, song)

        return songs

    @staticmethod
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


class Visualizations(object):

    def __init__(self, file_name,):
        self.file = file_name
        self.df = pd.DataFrame(pd.read_csv("./" + self.file, index_col=0))
        self.start = self.df["Week"].min()
        self.end = self.df["Week"].max()

        # self.appearances()

    def appearances(self):
        # Number of appearance of artists in billboard100
        num_appearances = self.df.groupby(["Artists"]).count()[["Songs"]].sort_values(by="Songs", ascending=False)
        num_appearances = num_appearances.reset_index()

        plt.style.use("ggplot")
        fig, ax = plt.subplots()
        bars = ax.barh(num_appearances.iloc[:10]["Artists"], num_appearances.iloc[:10]["Songs"],
                       color="maroon")
        ax.bar_label(bars)
        plt.xlabel("Number of Appearances")
        plt.title("Top Artist with most Appearance in Billboard100 \n"
                  "from {} to {}".format(self.start, self.end))
        plt.show()


if __name__ == '__main__':
    link = "https://www.billboard.com/charts/hot-100/{}/"
    file = "billboard100_2023-07-15_2023-05-20.csv"
    # Dataset(link, 8, "2023-07-15")
    Visualizations(file)
