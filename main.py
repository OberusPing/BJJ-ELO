from bs4 import BeautifulSoup
from selenium import webdriver

# Set up web driver
firefox_driver_path = 'geckodriver'
options = webdriver.FirefoxOptions()
options.add_argument("headless")
driver = webdriver.Firefox(
    executable_path=firefox_driver_path, options=options)

driver.get("http://www.bjjheroes.com/a-z-bjj-fighters-list")
page_source = driver.page_source

# Scrape list of bjj fighters and links to bjj-hero page, put it in an array
# data: [[first_name, last_name, nickname(optional), team(optional)]]
soup = BeautifulSoup(page_source, 'lxml')

data = []
table = soup.find(
    'table', attrs={'class': 'tablepress tablepress-id-104 dataTable no-footer'})

table_body = table.find('tbody')

rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols])

# Create an array of match histories (wins and losses) for each fighter

# Get Elo ratings
