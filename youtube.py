import time, os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from youtube_title_parse import get_artist_title

class Youtube:
    def __init__(self, p_url):
        self.path = os.getcwd() + os.sep + 'chromedriver'
        self.playlist_url = p_url
        self.songs_info = {}

    def get_songs_title(self):
        driver = webdriver.Chrome(self.path)
        driver.get(self.playlist_url)
        delay = 20
        try:
            WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.ID, 'playlist-items')))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        vids = soup.find_all(id='playlist-items')
        song_titles = []
        for vid in vids:
            title = vid.find(id='video-title')
            song_titles.append(title.get('title'))
        driver.quit()
        return song_titles

    def get_songs_info(self, song_titles):
        for song_title in song_titles:
            val = get_artist_title(song_title)
            if val:
                artist, title = val
                if '&' in artist:
                    artist = artist.split('&')[0]
                if '(' in title:
                    title = title.split('(')[0]
                self.songs_info[title] = artist
            else:
                print(f"{song_title} cannot be parsed!")

        return self.songs_info
