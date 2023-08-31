# companies_house
Scrape data from Companies House

⚠ **Important!!**

Use the script responsibly as this pings a government website.
- Use the official API instead if calling on the script multiple times.
- Do not put undue stress on their servers. Minimise data extraction and use time delays.
- Check their robots.txt file .

Given a search term (e.g. last name) it will aggregate all the data into a clean tabular format that can be used for further analysis

Example use case:
E.g. Find all officers that have last name "Smith" from Swansea.
1) Use the script with search_term = "Smith" to collate officers in clean tabular format
2) Use the Address column of the resulting table to narrow the search to addresses that include Swansea.
