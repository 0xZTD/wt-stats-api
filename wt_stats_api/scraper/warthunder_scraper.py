from enum import Enum
from typing import List, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from dataclasses import dataclass


# --- Data Structures ---
class GameMode(Enum):
    ARCADE = "arcade"
    REALISTIC = "realistic"
    SIM = "simualtion"


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
    game_mode: Optional[GameMode] = None


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
    game_mode: Optional[GameMode] = None


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
    game_mode: Optional[GameMode] = None


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
    game_mode: Optional[GameMode] = None


@dataclass
class NationStats:
    nation: str
    vehicles_total: str
    vehicles_spaded: str
    rewards: str


class StatTabs(Enum):
    REALISTIC = "user-stat__list historyFightTab"
    # first tab has is-visible class by default for some reason
    ARCADE = "user-stat__list arcadeFightTab is-visible"
    SIM = "user-stat__list simulationFightTab"


class AirStatTabs(Enum):
    REALISTIC = ""
    ARCADE = "user-stat__list arcadeFightTab is-visible"
    SIM = ""


BASE_URL = "https://warthunder.com"
SEARCH_URL = "https://warthunder.com/en/community/searchplayers"
SEARCH_LINK = SEARCH_URL + "?name="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/110.0.0.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


# --- Main logic ---
def get_player_link(name: str) -> dict:
    links_map = {}
    driver = uc.Chrome(headless=False)

    driver.get(SEARCH_LINK + name)

    wait = WebDriverWait(driver, 15)  # Maximum wait time of 15 seconds
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "scp_td2")))
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    for td in soup.find_all("td", class_="scp_td2"):
        for unit in td.find_all("a"):
            link = unit.get("href")
            nick = unit.text.strip()
            links_map[nick] = link
    driver.close()
    return links_map


def get_correct_name(links_map: dict) -> str:
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


def get_user_pick(range: int) -> int:
    while True:
        try:
            pick = input(f"\nInput correct number, between 1 and {range}:")
            pick = int(pick)
            if pick < 0 or pick > range:
                print("\nSpecify correct range")
                continue
            return pick
        except (TypeError, ValueError):
            print("\nOnly correct numbers allowed, try again.")


def visit_user_page(player_link: str) -> list:
    driver = uc.Chrome(headless=False)

    driver.get(BASE_URL + player_link)

    wait = WebDriverWait(driver, 15)  # Maximum wait time of 15 seconds
    element = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "user-profile__data-nick"))
    )
    html = driver.page_source

    arcade_stats = get_user_stat(StatTabs.ARCADE, html)
    realistic_stats = get_user_stat(StatTabs.REALISTIC, html)
    sim_stats = get_user_stat(StatTabs.SIM, html)
    ground_stats = get_ground_stats(html)
    air_stats = get_air_stats(html)
    naval_stats = get_naval_stats(html)
    nations_stats = get_nations_stats(html)
    stats = {
        "arcade_stats": arcade_stats,
        "realistic_stats": realistic_stats,
        "sim_stats": sim_stats,
        "ground_stats": ground_stats,
        "air_stats": air_stats,
        "naval_stats": naval_stats,
        "nations": nations_stats,
    }
    driver.close()
    return stats


def get_air_stats(html: str) -> List[AirBattleStats]:
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find("div", class_="user-rate__fightType")

    arcade_li = div.find("ul", class_=StatTabs.ARCADE.value).find_all("li")
    realistic_li = div.find("ul", class_=StatTabs.REALISTIC.value).find_all("li")
    sim_li = div.find("ul", class_=StatTabs.SIM.value).find_all("li")

    lists = [arcade_li, realistic_li, sim_li]
    stats = []
    for li_list in lists:
        stats.append(
            AirBattleStats(
                li_list[0].text,
                li_list[1].text,
                li_list[2].text,
                li_list[3].text,
                li_list[4].text,
                li_list[5].text,
                li_list[6].text,
                li_list[7].text,
                li_list[8].text,
                li_list[9].text,
                li_list[10].text,
                li_list[11].text,
            )
        )
    stats[0].game_mode = GameMode.ARCADE
    stats[1].game_mode = GameMode.REALISTIC
    stats[2].game_mode = GameMode.SIM

    keys = ["air_arcade", "air_realistic", "air_sim"]
    dict_stats = dict(zip(keys, stats))
    return dict_stats


def get_ground_stats(html: str) -> List[GroundBattleStats]:
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find("div", class_="user-rate__fightType")
    current_div = div.find_all("div", class_="user-stat__list-row")[1]

    arcade_li = current_div.find("ul", class_=StatTabs.ARCADE.value).find_all("li")
    realistic_li = current_div.find("ul", class_=StatTabs.REALISTIC.value).find_all(
        "li"
    )
    sim_li = current_div.find("ul", class_=StatTabs.SIM.value).find_all("li")

    lists = [arcade_li, realistic_li, sim_li]
    stats = []
    for li_list in lists:
        stats.append(
            GroundBattleStats(
                li_list[0].text,
                li_list[1].text,
                li_list[2].text,
                li_list[3].text,
                li_list[4].text,
                li_list[5].text,
                li_list[6].text,
                li_list[7].text,
                li_list[8].text,
                li_list[9].text,
                li_list[10].text,
                li_list[11].text,
                li_list[12].text,
                li_list[13].text,
            )
        )
    stats[0].game_mode = GameMode.ARCADE
    stats[1].game_mode = GameMode.REALISTIC
    stats[2].game_mode = GameMode.SIM
    keys = ["ground_arcade", "ground_realistic", "ground_sim"]
    dict_stats = dict(zip(keys, stats))
    return dict_stats


def get_naval_stats(html: str) -> List[NavalBattleStats]:
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find("div", class_="user-rate__fightType")
    current_div = div.find_all("div", class_="user-stat__list-row")[2]

    arcade_li = current_div.find("ul", class_=StatTabs.ARCADE.value).find_all("li")
    realistic_li = current_div.find("ul", class_=StatTabs.REALISTIC.value).find_all(
        "li"
    )
    sim_li = current_div.find("ul", class_=StatTabs.SIM.value).find_all("li")

    lists = [arcade_li, realistic_li, sim_li]
    stats = []
    for li_list in lists:
        stats.append(
            NavalBattleStats(
                li_list[0].text,
                li_list[1].text,
                li_list[2].text,
                li_list[3].text,
                li_list[4].text,
                li_list[5].text,
                li_list[6].text,
                li_list[7].text,
                li_list[8].text,
                li_list[9].text,
                li_list[10].text,
                li_list[11].text,
                li_list[12].text,
                li_list[13].text,
                li_list[14].text,
                li_list[15].text,
                li_list[16].text,
                li_list[17].text,
                li_list[18].text,
                li_list[19].text,
            )
        )

    stats[0].game_mode = GameMode.ARCADE
    stats[1].game_mode = GameMode.REALISTIC
    stats[2].game_mode = GameMode.SIM
    keys = ["naval_arcade", "naval_realistic", "naval_sim"]
    dict_stats = dict(zip(keys, stats))
    return dict_stats


def get_user_stat(tab: StatTabs, html: str) -> WarThunderStats:
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
    match (tab):
        case tab.ARCADE:
            stats.game_mode = GameMode.ARCADE
        case tab.REALISTIC:
            stats.game_mode = GameMode.REALISTIC
        case tab.SIM:
            stats.game_mode = GameMode.SIM

    return stats


def get_nations_stats(html: str) -> List[NationStats]:
    soup = BeautifulSoup(html, "html.parser")
    # wrapper div
    div = soup.find("div", class_="user-profile__score user-score")
    ul_titles = div.find("ul", class_="user-score__list-title")
    ul_total_vehicles = ul_titles.find_next_sibling("ul")
    ul_spaded_vehicles = ul_total_vehicles.find_next_sibling("ul")
    ul_awards = ul_spaded_vehicles.find_next_sibling("ul")

    nations: List[NationStats] = []
    for i in range(1, len(ul_titles.find_all("li"))):
        nations.append(
            NationStats(
                ul_titles.find_all("li")[i].text.strip(),
                ul_total_vehicles.find_all("li")[i].text,
                ul_spaded_vehicles.find_all("li")[i].text,
                ul_awards.find_all("li")[i].text,
            )
        )
        pass

    return nations


def run():
    name = input("Specify name for search:\n")
    choice = get_player_link(name)
    link = get_correct_name(choice)
    print(visit_user_page(link))


if __name__ == "__main__":
    test_link = "/community/userinfo/?nick=ztdd%231"
    # choice = get_player_link("ztdd")
    # link = get_correct_name(choice)
    print(visit_user_page(test_link))
