import pandas as pd
from bs4 import BeautifulSoup
import re
import requests
from datetime import datetime
import os

url = "https://travel.state.gov/content/travel/en/us-visas/visa-information-resources/list-of-posts.html"
headers = {
        'User-Agent': 'My User Agent 1.0',
        'From': 'https://github.com/Leschonander/StateDepartmentVisaScraper'  
    }

data = pd.read_csv("StateDepartmentVisaLocations.csv")

def query_visa_times(cid: str):

    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36',
        'sec-ch-ua-platform': '"Android"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://travel.state.gov/content/travel/en/us-visas/visa-information-resources/wait-times.html',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    params = (
        ('cid', cid),
        ('aid', 'VisaWaitTimesHomePage'),
    )

    response = requests.get('https://travel.state.gov/content/travel/resources/database/database.getVisaWaitTimes.html', headers=headers, params=params)

    data = response.text.replace("\r", "").replace("\n", "")
    data = data.split(",")
    
    visa_dates = {
        "Vistor Visa Times": data[0].replace(" Days", ""),
        "Student & Vistor Exchange Visa Times": data[1].replace(" Days", ""),
        "All Other Non-Immigrant Visa Times": data[2].replace(" Days", ""),
    }

    return visa_dates

records = []
for i, row in enumerate(data.itertuples(index=False)):
    data = query_visa_times(row[1])
    data["Date Scraped"] =  datetime.today().strftime("%Y-%m-%d")
    data["Location"] = row[0]
    records.append(data)


if os.path.exists("./data/WaitTimes.csv") == True:
    new_data = pd.DataFrame(records)
    old_data = pd.read_csv("./data/WaitTimes.csv")
    combined_data = pd.concat([new_data, old_data])
    print(combined_data)
    combined_data = combined_data[["Location","Date Scraped","Vistor Visa Times","Student & Vistor Exchange Visa Times", "All Other Non-Immigrant Visa Times"]]
    combined_data.to_csv("./data/WaitTimes.csv",  encoding='utf-8')
else:
    new_data = pd.DataFrame(records)
    print(new_data)
    new_data.to_csv("./data/WaitTimes.csv",  encoding='utf-8')