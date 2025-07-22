from pyvirtualdisplay import Display
from scraper.warthunder_scraper import run

# Start virtual display
display = Display(visible=1, size=(1920, 1080))
display.start()
run()
display.stop()
