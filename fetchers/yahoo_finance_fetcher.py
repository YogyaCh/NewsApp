import requests
from bs4 import BeautifulSoup
from helpers.parsing_helpers import clean_text


# Function to fetch and parse Yahoo Finance sectors
def fetch_yahoo_finance_quotations(ticker):
    url = "https://finance.yahoo.com/quote/"+ticker+"/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    quote = {}
    quote_statistics = soup.find('div', {'data-testid': 'quote-statistics'})
    
    if quote_statistics:
        for item in quote_statistics.find_all('li'):
            label = item.find('span', class_='label')
            value = item.find('span', class_='value')
            
            label_text = clean_text(label.text) if label else 'No label'
            value_text = clean_text(value.text) if value else 'No value'
            
            if label_text != 'No label': quote[label_text] = value_text 
    
    return quote