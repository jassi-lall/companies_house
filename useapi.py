import requests
from requests.auth import HTTPBasicAuth
from os import getenv
from time import sleep
import pandas as pd
import csv

database = "companies.csv"
fieldnames = ['Company number', 'Date of creation', 'Name']
attr = ['company_number', 'date_of_creation', 'company_name']

api_key = getenv('companies_house_api_key')
if api_key is None:
    print("No API key found. Save API key as environment variable 'companies_house_api_key'")
    exit()
auth = HTTPBasicAuth(api_key,'')

def clear_database():
    with open(database, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(fieldnames)
        # add two entries
        company6 = get_company(6)
        sleep(1)
        company86 = get_company(86)
        csv_writer.writerow([company6[key] for key in attr])
        csv_writer.writerow([company86[key] for key in attr])

def get_company(company_number):
    url = 'https://api.company-information.service.gov.uk/company/'
    if isinstance(company_number, int):
        url += f'{company_number:08d}'
    elif isinstance(company_number, str):
        url += company_number

    r = requests.get(url, auth=auth)
    if r.status_code != 200:
        return r.status_code
    else:
        return r.json()

def scan():
    # Find last company found
    # Another way of doing this is having a seperate .py file for variables like api_key, and last_company_found that is updated whenever scanning
    last_company = None
    with open(database, mode='r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        try:
            last_company = (list(csv_reader)[-1])[0]
        except:
            pass

    index = 0

    if last_company == None:
        companies = [get_company(n) for n in [6, 86]]
        index = 117
    else:
        index = int(last_company) + 1
    
    while True:
        sleep(1)
        company = get_company(index)
        if company == 404:
            print(f'{index:08d} status code: 404')
        elif isinstance(company, int):
            raise Exception(f"When looking for company {index} recieved unexpected status code: {company}")
        else:
            print(f"Found company number {company['company_number']} created on {company['date_of_creation']} named {company['company_name']}") 
            with open(database, mode='a', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow([company[attr] for attr in ['company_number', 'date_of_creation', 'company_name']])
                    
        index += 1

scan()