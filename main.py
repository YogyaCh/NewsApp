from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from fetchers.cnn_news_fetcher import fetch_cnn_news
from fetchers.yahoo_finance_fetcher import fetch_yahoo_finance_quotations

app = Flask(__name__)

DATA_DIR = 'data'

def load_json(file_name):
    with open(os.path.join(DATA_DIR, file_name), 'r') as file:
        return json.load(file)

def save_json(data, file_name):
    with open(os.path.join(DATA_DIR, file_name), 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def index():
    categories = load_json('categories.json')
    tickers = load_json('tickers.json')
    news = fetch_cnn_news(categories)
    ticker_data = {ticker: fetch_yahoo_finance_quotations(ticker) for ticker in tickers}
    return render_template('index.html', news=news, ticker_data=ticker_data, categories=categories)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        categories = request.form.getlist('categories')
        tickers = request.form.getlist('tickers')
        save_json(categories, 'categories.json')
        save_json(tickers, 'tickers.json')
        return redirect(url_for('index'))
    
    categories = load_json('categories.json')
    tickers = load_json('tickers.json')
    return render_template('settings.html', categories=categories, tickers=tickers)

if __name__ == '__main__':
    app.run(debug=True)
