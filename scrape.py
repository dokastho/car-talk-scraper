#!env/bin/python3

from pathlib import Path
from threading import Lock, Thread
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess

START_PAGE = 0

# Configure Selenium
#
# Pro-tip: remove the "headless" option and set a breakpoint.  A Chrome
# browser window will open, and you can play with it using the developer
# console.
options = webdriver.chrome.options.Options()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")

# chromedriver is not in the PATH, so we need to provide selenium with
# a full path to the executable.
node_modules_bin = subprocess.run(
    ["npm", "bin"],
    stdout=subprocess.PIPE,
    universal_newlines=True,
    check=True
)
node_modules_bin_path = node_modules_bin.stdout.strip()
chromedriver_path = Path(node_modules_bin_path) / "chromedriver"

driver = webdriver.Chrome(
    options=options,
    executable_path=str(chromedriver_path),
)

# start scraping

link = "https://www.wnyc.org/shows/car-talk"

ep_links = []

if START_PAGE != 0:
    link = f'{link}/{START_PAGE}'

driver.get(link)

while True:
    links = driver.find_elements_by_xpath('//a[@data-test-selector="story-tease-title"]')

    ep_links += [ln.get_attribute("href") for ln in links]
    
    try:
        next = driver.find_element_by_xpath('//span[@class="pagefooter-next"]')
        
        if next is not None:
            btn = next.find_element_by_xpath("//button")
            btn.click()
    except:
        break

with open("links.txt", "w") as fp:
    fp.writelines("\n".join(ep_links))
    fp.close()
