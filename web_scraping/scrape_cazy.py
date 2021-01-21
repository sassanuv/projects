import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_table_rows(url):
    page  = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    rows = soup.find('table',{"class":"listing"}).find_all('tr')
    return rows


def get_headers(url):
    headers = []
    rows = get_table_rows(url)
    headers = []

    # Headers is defined at 2nd index
    for item in rows[2].find_all('td'):
        headers.append(item.text)

    return headers

def generate_dictionary(rows, headers):
    results = []
    for row in rows[3:]:
        data = row.find_all('td')
        if len(data)  == len(headers):
            new = {}
            for index, item in enumerate(data):
                new[headers[index]] = item.text.rstrip().strip()

            results.append(new)


# URL for first page
base_url = 'http://www.cazy.org/GH18_eukaryota.html'

headers = get_headers(base_url)
rows = get_table_rows(base_url)
results = generate_dictionary(rows, headers)




df = pd.DataFrame(results).drop_duplicates()

df.to_csv('test.csv')
