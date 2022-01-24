import pandas as pd
from bs4 import BeautifulSoup
import re
import requests

url = "https://travel.state.gov/content/travel/en/us-visas/visa-information-resources/list-of-posts.html"
headers = {
        'User-Agent': 'My User Agent 1.0',
        'From': 'https://github.com/Leschonander/SenateVideoScraper'  
    }

res = requests.get(url, headers=headers)

soup =  BeautifulSoup(res.text,'html.parser')

locations = soup.find_all("a", href=re.compile("Supplements_by_Post"))
locations = [l.get_text() for l in locations]
locations = [l.split("-")[0].strip() for l in locations]

locations_df = pd.DataFrame(locations, columns=['Locations'])
locations_df.to_csv("StateDepartmentVisaLocations.csv")