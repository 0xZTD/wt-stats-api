from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth


BASE_URL = "https://warthunder.com"
SEARCH_URL = "https://warthunder.com/en/community/searchplayers"
SEARCH_LINK = SEARCH_URL + "?name="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/110.0.0.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def get_player_link(name):
    links_map = {}
    driver = uc.Chrome(headless=False)

    driver.get(SEARCH_LINK + name)

    wait = WebDriverWait(driver, 15)  # Maximum wait time of 15 seconds
    element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "scp_td2")))
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    for td in soup.find_all("td", class_="scp_td2"):
        for unit in td.find_all("a"):
            link = unit.get("href")
            nick = unit.text.strip()
            links_map[nick] = link
    return links_map


def get_correct_name(links_map):
    print("Pick correct name:")
    iter = 1
    for name, link in links_map.items():
        print(f"{iter}. {name}")
        iter += 1
    pick = get_user_pick(iter - 1)
    try:
        to_list = list(links_map)
        value = to_list[pick - 1]
        return links_map[value]
    except IndexError as e:
        print(e)
    return None


def get_user_pick(range):
    while True:
        try:
            pick = input(f"\nInput correct number, between 1 and {range}:")
            pick = int(pick)
            if pick < 0 or pick >= range:
                print("\nSpecify correct range")
                continue
            return pick
        except (TypeError, ValueError):
            print("\nOnly correct numbers allowed, try again.")


if __name__ == "__main__":
    choice = get_player_link("ztdd")
    print(get_correct_name(choice))
