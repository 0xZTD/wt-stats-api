from pyvirtualdisplay import Display
from wt_stats_api.scraper import warthunder_scraper


def run():
    # Start virtual display
    display = Display(visible=0, size=(1920, 1080))
    display.start()
    warthunder_scraper.run()
    display.stop()


def get_player_link(name: str) -> dict:
    display = Display(visible=0, size=(1920, 1080))

    display.start()
    data = warthunder_scraper.get_player_link(name)
    display.stop()

    return data


def get_user_stats_by_url(url: str):
    display = Display(visible=0, size=(1920, 1080))

    display.start()
    data = warthunder_scraper.visit_user_page(url)
    display.stop()

    return data


if __name__ == "__main__":
    run()
