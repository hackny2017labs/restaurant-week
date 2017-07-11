import re

import bs4
import requests


def extract_as_number(text):
    exp = re.compile(r'\d+')
    return exp.search(text).group(0)

current_page = 'https://www.opentable.com/promo.aspx?pid=69&m=8'

response = requests.get(current_page)
if response.status_code != 200:
    raise Exception('Invalid response for {}'.format(current_page))

"""
div.content-section-list
  div.result.content-section-list-row
    div.rest-row
      div.rest-row-image
      div.rest-row-info
"""

text = response.text
beautified_response = bs4.BeautifulSoup(text)
section_list = beautified_response.find('div', class_='content-section-list')
rows = section_list.find_all('div', class_='content-section-list-row')

restaurants = []

for row in rows:
    info = row.find('div', class_='rest-row-info')
    context = {
        'name': None,
        'type': None,
        'reviews': {
            'count': None,
            'percent_recommended': None
        },
        'location': None,
        'promo_message': None
    }

    context['name'] = info.find('span', class_='rest-row-name-text').text
    context['type'] = info.find('span', class_='rest-row-meta--cuisine').text
    context['reviews']['count'] = extract_as_number(info.find('span', class_='rest-row-meta--location').text)
    context['reviews']['percent_recommended'] = extract_as_number(info.find('span', class_='recommended-small').text)
    context['location'] = info.find('span', class_='rest-row-meta--location').text
    context['promo_message'] = info.find('div', class_='rest-promo-message').text

    restaurants.append(context)
