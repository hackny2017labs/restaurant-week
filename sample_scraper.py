import urllib2
import json
import pandas as pd

michelins = []
with open('michelin.txt') as f:
    lines = f.read().splitlines()

url = 'https://www.nycgo.com/feed?vertical=restaurantWeek&entryId=179'
response = urllib2.urlopen(url)

html = response.read()
result = json.loads(html)

cuisines_dict = {}
for x in result['lookups']['cuisines']:
    cuisines_dict[x['id']] = x['title']

neighborhoods_dict = {}
for x in result['lookups']['neighborhoods']:
    neighborhoods_dict[x['id']] = x['title']

restaurants = result['entries'][0]['participants']
df = []
for x in restaurants:
    name = x['title']
    meals = x['meals'].split("|")
    cuisines = [cuisines_dict[c] for c in x['cuisine']]
    neighborhood = neighborhoods_dict[x['neighborhood'][0]]

    df.append(
        [name, cuisines, meals, neighborhood]
    )

df = pd.DataFrame(df)
print df.head()
