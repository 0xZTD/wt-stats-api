from enum import Enum
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from dataclasses import dataclass


# WarThunderStats is general stats class, not detailed stat per game mode
@dataclass
class WarThunderStats:
    victories: str
    completed_missions: str
    winrate: str
    deaths: str
    lions_earned: str
    play_time: str
    air_targets_destroyed: str
    ground_targets_destroyed: str
    naval_targets_destroyed: str


@dataclass
class AirBattleStats:
    air_battles: str
    air_battles_fighter: str
    air_battles_bomber: str
    air_battles_attacker: str
    time_played_air_battles: str
    time_played_fighter: str
    time_played_bomber: str
    time_played_attacker: str
    total_targets_destroyed: str
    air_targets_destroyed: str
    ground_targets_destroyed: str
    naval_targets_destroyed: str


@dataclass
class GroundBattleStats:
    ground_battles: str
    ground_battles_tank: str
    ground_battles_spg: str
    ground_battles_heavy_tank: str
    ground_battles_spaa: str
    time_played_ground_battles: str
    tank_battle_time: str
    tank_destroyer_battle_time: str
    heavy_tank_battle_time: str
    spaa_battle_time: str
    total_targets_destroyed: str
    air_targets_destroyed: str
    ground_targets_destroyed: str
    naval_targets_destroyed: str


@dataclass
class NavalBattleStats:
    naval_battles: str
    ship_battles: str
    motor_torpedo_boat_battles: str
    motor_gun_boat_battles: str
    motor_torpedo_gun_boat_battles: str
    sub_chaser_battles: str
    destroyer_battles: str
    naval_ferry_barge_battles: str
    time_played_naval: str
    time_played_ship: str
    time_played_motor_torpedo_boat: str
    time_played_motor_gun_boat: str
    time_played_motor_torpedo_gun_boat: str
    time_played_sub_chaser: str
    time_played_destroyer: str
    time_played_naval_ferry_barge: str
    total_targets_destroyed: str
    air_targets_destroyed: str
    ground_targets_destroyed: str
    naval_targets_destroyed: str


@dataclass
class NationStats:
    vehicles_total: str
    vehicles_spaded: str
    rewards: str


@dataclass
class NationVehiclesRewards:
    usa: NationStats
    ussr: NationStats
    great_britain: NationStats
    germany: NationStats
    japan: NationStats
    italy: NationStats
    france: NationStats
    china: NationStats
    sweden: NationStats
    israel: NationStats


class StatTabs(Enum):
    REALISTIC = "user-stat__list historyFightTab"
    # first tab has is-visible class by default for some reason
    ARCADE = "user-stat__list arcadeFightTab is-visible"
    SIM = "user-stat__list simulationFightTab"


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
    driver.close()
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


def visit_user_page(player_link):
    driver = uc.Chrome(headless=False)

    driver.get(BASE_URL + player_link)

    wait = WebDriverWait(driver, 15)  # Maximum wait time of 15 seconds
    element = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "user-profile__data-nick"))
    )
    html = driver.page_source

    stats = []
    arcade_stats = get_user_stat(StatTabs.ARCADE, html)
    realistic_stats = get_user_stat(StatTabs.REALISTIC, html)
    sim_stats = get_user_stat(StatTabs.SIM, html)
    stats.extend([arcade_stats, realistic_stats, sim_stats])

    return stats


def get_user_stat(tab, html):
    soup = BeautifulSoup(html, "html.parser")
    ul = soup.find("ul", class_=tab.value)
    li_list = ul.find_all("li")

    # each li has no distinct css class, so just indexing
    stats = WarThunderStats(
        li_list[1].text,
        li_list[2].text,
        li_list[3].text,
        li_list[4].text,
        li_list[5].text,
        li_list[6].text,
        li_list[7].text,
        li_list[8].text,
        li_list[9].text,
    )
    return stats


if __name__ == "__main__":
    test_link = "/community/userinfo/?nick=ztdd%231"
    # choice = get_player_link("ztdd")
    # link = get_correct_name(choice)
    print(visit_user_page(test_link))
