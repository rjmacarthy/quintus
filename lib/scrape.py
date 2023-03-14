import os
import json
import requests
import pydash as _

URL = os.environ.get('URL')


class ArticleScraper:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def write_article(self, article):
        article_id = article['id']
        with open(os.path.join(self.output_dir, f'article{article_id}.json'), 'w') as article_file:
            article_file.write(json.dumps({
                'id': _.get(article, 'id'),
                'title': _.get(article, 'title'),
                'body': _.get(article, 'body'),
                'url': _.get(article, 'url'),
            }))

    def get_page(self, page_number):
        page_url = f"{URL}?page={page_number}"
        response = requests.get(page_url)
        data = response.json()
        return data

    def scrape(self):
        page_number = 1
        while True:
            data = self.get_page(page_number)
            articles = data.articles
            if len(articles) == 0:
                break
            for article in articles:
                self.write_article(article)
            page_number += 1
