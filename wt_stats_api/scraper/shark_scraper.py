from bs4 import BeautifulSoup
from base import MY_ID
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc


URL = "https://statshark.net/player/"


def get_page():
    driver = uc.Chrome(headless=False)
    driver.get(URL + MY_ID)
    wait = WebDriverWait(driver, 15)  # Maximum wait time of 15 seconds
    html = driver.page_source

    soup = BeautifulSoup(html.text, "html.parser")
    title = soup.find("span", class_="player-info__title")
    print(title)


if __name__ == "__main__":
    get_page()
