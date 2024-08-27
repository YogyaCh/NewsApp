import requests
from bs4 import BeautifulSoup
from helpers.parsing_helpers import clean_text, get_category_from_url

# Function to fetch and parse CNN news sitemap
def fetch_cnn_news():
    url = "https://www.cnn.com/sitemap/news.xml"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    news_items = soup.find_all('url')
    
    news_data = []
    for item in news_items[:5]:  # Limiting to first 5 news articles for brevity
        news_url = item.find('loc').text
        publication_date = item.find('news:publication_date').text if item.find('news:publication_date') else 'No date'
        
        news_response = requests.get(news_url)
        news_soup = BeautifulSoup(news_response.content, 'html.parser')
        title = news_soup.find('h1').text if news_soup.find('h1') else 'No title'
        summary = news_soup.find('meta', {'name': 'description'})['content'] if news_soup.find('meta', {'name': 'description'}) else 'No summary'
        
        # Clean up title and summary
        title = clean_text(title)
        summary = clean_text(summary)
        
        category = get_category_from_url(news_url)
        
        if title != 'No title':
            news_data.append({'title': title, 'summary': summary, 'category': category, 'url': news_url, 'publication_date': publication_date})
    
    return news_data