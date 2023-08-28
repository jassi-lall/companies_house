""" 
Search officers in companies house.

! IMPORTANT !
Use the script responsibly as this pings a government website.
- Use the official API instead if calling on the script multiple times.
- Do not put undue stress on their servers. Minimise data extraction and use time delays.
- Check their robots.txt file . Suggested crawl delay 10.

Given a search term (e.g. last name) it will aggregate all the data into a clean tabular format that can be used for further analysis

Example use case:
E.g. Find all officers that have last name "Smith" from Swansea.
1) Use the script with search_term = "Smith" to collate officers in clean tabular format
2) Use the Address column of the resulting table to narrow the search to addresses that include Swansea.

"""
from bs4 import BeautifulSoup # Parse HTML tags
import requests # request resources from internet server
import pandas as pd # tabular data analysis
from time import sleep # crawl delay
import random # randomise crawl delay

officer_data = [] # A list of dicts that have the same format {"name":val, "no_of_appointments":val, "link":val, "address":val}

#search_term = input("Enter search term: ")
search_term = "fhalora"

page_no = 1
while(True):
    url = f"https://find-and-update.company-information.service.gov.uk/search/officers?q={search_term}&page={page_no}"
    request = requests.get(url)
    if request.status_code != 200:
        break
    print(f"... scanning page {page_no}")
    sleep(1 + random.uniform(1,3)) # Do NOT remove crawl delay
    soup = BeautifulSoup(request.content, "lxml")

    officers = soup.find_all("li", {"class": "type-officer"})
    if len(officers) == 0:
        break
    for officer in officers:
        officer_info = officer.text.strip().split("\n") # Yields list in the form [name, total no of appointments, address]
        officer_link = officer.find("a")

        officer_data.append(
            {
                "name": officer_info[0],
                "no_of_appointments": officer_info[1],
                "link": officer_link.get("href"),
                "address": officer_info[2],
            }
        )
    page_no += 1

df = pd.DataFrame.from_records(officer_data)
print(df.head())
