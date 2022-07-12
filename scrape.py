#!env/bin/python3

from pathlib import Path
from selenium import webdriver
import subprocess

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

LINK = "https://www.wnyc.org/shows/car-talk"

ep_links = []

page_num = 0

while page_num < 50:

    link = f'{LINK}/{page_num}'
    driver.get(link)

    driver.implicitly_wait(3)
    links = driver.find_elements_by_xpath('//a[@data-test-selector="story-tease-title"]')

    new_links = [ln.get_attribute("href") for ln in links]

    [print(f'Get: {len(ep_links) + i} {ln}') for i, ln in enumerate(new_links)]

    ep_links += new_links

    page_num += 1

with open("links.txt", "w") as fp:
    fp.writelines("\n".join(ep_links))
    fp.close()
