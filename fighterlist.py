from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import json


# Set up web driver
firefox_driver_path = 'geckodriver'
options = FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(
    executable_path=firefox_driver_path, options=options)

driver.get("http://www.bjjheroes.com/a-z-bjj-fighters-list")
page_source = driver.page_source

# Scrape list of bjj fighters and links to bjj-hero page, put it in an array
# data: [[first_name, last_name, nickname(optional), team(optional)]]
soup = BeautifulSoup(page_source, 'lxml')

data = {}
table = soup.find(
    'table', attrs={'class': 'tablepress tablepress-id-104 dataTable no-footer'})

table_body = table.find('tbody')

rows = table_body.find_all('tr')
fighter_id = 0

for row in rows:
    try:
        fighter_link = row.find('a')['href']
        if not fighter_link.startswith('http'):
            fighter_link = 'http://bjjheroes.com' + fighter_link
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        cols.append(fighter_link)
        cols.insert(0, fighter_id)
        fighter_name = cols[1] + cols[2]

        data[fighter_name] = cols
        fighter_id += 1

    except (TypeError):
        pass

# Create an array of match histories (wins and losses) for each fighter

for el in data:
    try:
        fighter_link = data[el][-1]
        driver.get(fighter_link)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        table = soup.find(
            'table', attrs={'class': 'table table-striped sort_table dataTable no-footer'})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            opponent_name = cols[0].replace(" ", "")
        data[el].append(cols)

    except (TypeError, AttributeError):
        pass

    with open('bjj-data.json', 'w') as fp:
        json.dump(data, fp)
