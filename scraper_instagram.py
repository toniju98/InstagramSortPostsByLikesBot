from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from login_instagram import username, password
from time import sleep
import pandas as pd
import json
import re


class SortByLikesBot:
    """Bot that sorts posts of an IG account by likes and writes it into a json file
    """

    def __init__(self, username, password):
        """Login and some necessary clicks at the beginning
        """
        executable_path = "your_chromedriver_path"
        self.browser = webdriver.Chrome(executable_path)
        self.links = []
        self.likes = []
        self.username = username
        self.password = password
        self.login()

    def sort_posts_by_likes(self, website):
        """Whole process of getting all likes of videos and images of one IG account and sorting them by number of likes

        :param website: the IG account we analyze
        :return:
        """
        self.browser.get(website)
        self.scroll(20)
        self.link_articles()
        data = self.create_dataframe()
        data_videos = self.check_data(data, "Aufrufe")
        data_img = self.check_data(data, "Gefällt")
        json_data_img = self.convert_to_json(data_img)
        json_data_vid = self.convert_to_json(data_videos)
        self.save_json("your_path", json_data_img)
        self.save_json("your_path", json_data_vid)

    def check_data(self, data, column_1):
        """Divide the dataset by video and image in two new dataframes, extracting numbers and sorting ascending

        :param data: the dataframe at the beginning with all data
        :param column_1: the type of data we want to extract
        :return: data_videos: new sorted dataframe
        """
        data["check"] = [column_1 in x for x in data["Likes"]]
        data_videos = data[(data["check"] == True)]
        data_videos["Num"] = [re.sub('\D', '', vid) for vid in data_videos["Likes"]]
        data_videos = data_videos.sort_values(by="Num", ascending=False)
        return data_videos

    def convert_to_json(self, data):
        """"Converting dataframe to json

        :return: json_videos_data: converted json
        """
        data_videos_to_json = data.to_json(orient='records', indent=4, force_ascii=False)
        json_videos_data = json.loads(data_videos_to_json)
        return json_videos_data

    def save_json(self, path, data):
        """Save json to a specified path

        :param path: file path
        :param data: dataset we want to save
        :return:
        """
        with open(path, "w", encoding="utf8") as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)

    def create_dataframe(self):
        """creates a dataframe with the links to the posts and the likes

        :return: data: dataframe
        """
        data = pd.DataFrame(columns=["Links", "Likes"])
        print(self.get_links())
        print(self.get_likes())
        data["Links"] = self.get_links()
        data["Likes"] = self.get_likes()
        return data

    def login(self):
        """Login process at the beginning

        :return:
        """
        newspaper_url = 'https://instagram.com/'
        # Get on instagram
        self.browser.get(newspaper_url)
        # Click on Cookie button
        WebDriverWait(self.browser, 40).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             'body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.bIiDR'))).click()
        # Insert username
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#loginForm > div > div:nth-child(1) > div > label > input"))).send_keys(self.username)
        # Insert password
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#loginForm > div > div:nth-child(2) > div > label > input"))).send_keys(self.password)
        # Login button
        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             '#loginForm > div > div:nth-child(3) > button'))).click()
        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             '#react-root > section > main > div > div > div > div > button'))).click()
        WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             'body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm'))).click()

    def do_it(self):
        """Scrape the links to the posts and append them to links list

        :return:
        """
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        articles = soup.find("article", "ySN3v")
        articles_2 = articles.find_all("div", "Nnq7C weEfm")
        for x in articles_2:
            new_list = x.find_all("div", "v1Nh3 kIKUG _bz0w")
            for i in new_list:
                b = i.find("a", href=True)
                self.links.append("https://instagram.com/" + b['href'])

    def link_articles(self):
        """Iterate through all links in the links list and scrape the likes from the post page

        :return:
        """
        links_list = []
        likes_list = []
        # unique links
        unique_links = list(set(self.links))
        for link in unique_links:
            links_list.append(link)
            # get on post page
            self.browser.get(link)
            soap = BeautifulSoup(self.browser.page_source, 'html.parser')
            if soap.find_all("span", "vcOH2"):
                y = soap.find(
                    'span', "vcOH2").get_text()
                if "Aufrufe" in y:
                    likes_list.append(y)
            if soap.find_all("button", "sqdOP yWX7d _8A5w5"):
                l = soap.find("button", "sqdOP yWX7d _8A5w5").get_text()
                if "Gefällt" in l:
                    likes_list.append(l)
        self.links = links_list
        self.likes = likes_list

    def scroll(self, timeout):
        """Scrolling through the posts and scraping meanwhile

        :param timeout: pause between each scroll action for loading the content
        :return:
        """
        scroll_pause_time = timeout

        # Get scroll height
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        self.do_it()

        while True:
            # Scroll down to bottom
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.do_it()
            # Wait to load page
            sleep(scroll_pause_time)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # If heights are the same it will exit the function
                break
            last_height = new_height

    def get_links(self):
        """Returns the links

        :return: self.links
        """
        return self.links

    def get_likes(self):
        """Returns the likes

        :return: self.likes
        """
        return self.likes


if __name__ == '__main__':
    scraper = SortByLikesBot(username, password)
	#TODO: link to the account you want to analyze
    scraper.sort_posts_by_likes("link_to_account")
