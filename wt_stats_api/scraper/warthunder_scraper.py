import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth


BASE_URL = "https://warthunder.com/en/community/searchplayers"
SEARCH_LINK = BASE_URL + "?name="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/110.0.0.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def get_player_link(name):
    driver = uc.Chrome(headless=False)

    driver.get(SEARCH_LINK + name)

    wait = WebDriverWait(driver, 15)  # Maximum wait time of 15 seconds
    element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "scp_td2")))
    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")
    for td in soup.find_all("td", class_="scp_td2"):
        print(td)
        for link in td.find_all("a"):
            print(link.get("href"))


if __name__ == "__main__":
    get_player_link("ztdd")
