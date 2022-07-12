#!env/bin/python3

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import subprocess
from pathlib import Path
import urllib.request

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

dl_links = []

with open("links.txt", "r") as fp:
    dl_links = fp.readlines()
    
threads = []

for i, page in enumerate(dl_links):
    page = page.strip()
    print(f'Get: {i} {page}')
    
    # set up file name
    name = page.lstrip("http://www.wnyc.org/story/")
    name = name.rstrip("/")
    name = "downloads" + name + ".mp3"
    
    # get link from page
    driver.get(page)
    
    driver.implicitly_wait(2)
    # a = ActionChains(driver)
    # dd_elt = driver.find_element_by_xpath('//div[@class="ember-basic-dropdown ember-view"]')
    # dd_btn = dd_elt.find_element_by_tag_name("button")
    # a.move_to_element(dd_elt).perform()
    dd_btn = driver.find_element_by_xpath('//div[@class="nypr-story-audio-options ember-view"]')
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(dd_btn, 18, 18)
    action.click()
    action.perform()
    
    link_elt = driver.find_element_by_xpath('//a[@class="panel-link link--dark text--medium"]')
    link = link_elt.get_attribute("href")
    
    try:
        urllib.request.urlretrieve(page,name)
    except:
        # replace url with "edge2.pod.npr.org"
        link_li = link.split("/")
        link_li[2] = "edge2.pod.npr.org"
        link = link_li.join()
        
        urllib.request.urlretrieve(page,name)
    
