from bs4 import BeautifulSoup
import requests
import pandas as pd

URL = 'https://www.audible.com/search?keywords=book&node=18573211011'

response = requests.get(url=URL)

web = response.text

soup = BeautifulSoup(web, 'html.parser')

prices = []
titles = []
subtitles = []
authors = []
narrateds = []
rutintimes = []
releases = []
lenguages = []
starts = []
ratings = []

items = soup.select('div.bc-col-responsive.bc-col-9 li.bc-list-item.productListItem')
    
for item in items:

    titles.append(item.select_one('li.bc-list-item h3 a').get_text().strip())
    authors.append(item.select_one('li.bc-list-item.authorLabel a').get_text().strip())
    narrateds.append(item.select_one('li.bc-list-item.narratorLabel a').get_text().strip())
    rutintimes.append(item.select_one('li.bc-list-item.runtimeLabel span').get_text().strip())
    releases.append(item.select_one('li.bc-list-item.releaseDateLabel span').get_text().replace('"','').replace('Release date:\n','').strip())
    lenguages.append(item.select_one('li.bc-list-item.languageLabel span').get_text().replace('"','').replace('Language:\n','').strip())
    starts.append(item.select_one('li.bc-list-item.ratingsLabel span.bc-pub-offscreen').get_text().strip())
    ratings.append(int(item.select_one('li.bc-list-item.ratingsLabel span.bc-color-secondary').get_text().strip().replace(',','').replace('ratings','')))
    prices.append(float(item.select_one('div.bc-col-responsive.bc-col-4 div#adbl-buy-box div.bc-row p.buybox-regular-price').get_text().replace('Regular price: \n\n', '').replace('$','').replace('\n        \n\n            or 1 credit', '').strip()))
    try:
        subtitles.append(item.select_one('li.bc-list-item.subtitle').get_text().strip())
    except:
        subtitles.append(None)
        print('Error subtitle')

dict_audible = {
    'title': titles,
    'subtitle': subtitles,
    'author': authors,
    'narrated': narrateds,
    'length': rutintimes,
    'release_date': releases,
    'lenguage': lenguages,
    'start': starts,
    'rating': ratings,
    'price': prices
}

df_audible = pd.DataFrame(dict_audible)

df_audible.to_csv("data_web_audiable.csv")

print("Data successfully")
