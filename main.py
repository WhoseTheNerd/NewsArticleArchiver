import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
import wget


#URL = "https://arstechnica.com/tech-policy/2021/05/att-overcharged-washington-dc-for-5-years-must-pay-1-5-million-ag-says/"
from ArsTechnica import ArsTechnica
from EFF import EFF
from Vice import Vice

URL = "https://www.eff.org/deeplinks/2020/12/raid-covid-whistleblower-florida-shows-need-reform-overbroad-computer-crime-laws"

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

domain_table = {
    "arstechnica.com": ArsTechnica(),
    "www.vice.com": Vice(),
    "www.eff.org": EFF()
}

domain = urlparse(URL).netloc
parser = domain_table[domain]

html_page = parser.update(URL, soup)

with open('article.html', 'wb') as f:
    f.write(html_page.prettify().encode())

print("Done")