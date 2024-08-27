def clean_text(text):
    return ' '.join(text.split()).replace('\\n', '').strip()

def get_category_from_url(url, categories):
    for category in categories:
        if category in url.lower():
            return category.capitalize()
    return 'Uncategorized'