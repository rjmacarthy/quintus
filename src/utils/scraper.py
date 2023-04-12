import os
import json
import requests
import pydash as _


class Scraper:
    def __init__(self, data_dir):
        self.url = None
        self.filters = None
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def filter_result(self, article) -> bool:
        return True in [f(article) for f in self.filters]

    def write_article(self, article):
        article_id = article["id"]
        with open(
            os.path.join(self.data_dir, f"article{article_id}.json"), "w"
        ) as article_file:
            article_file.write(
                json.dumps(
                    {
                        "id": _.get(article, "id"),
                        "title": _.get(article, "title"),
                        "body": _.get(article, "body"),
                        "url": _.get(article, "url"),
                    }
                )
            )

    def get_page(self, page_number):
        page_url = f"{self.url}?page={page_number}"
        response = requests.get(page_url)
        data = response.json()
        return data

    def scrape(self, url, filters):
        self.url = url
        self.filters = filters
        page_number = 1
        while True:
            data = self.get_page(page_number)
            articles = data["articles"]
            if len(articles) == 0:
                break
            for article in articles:
                if not self.filter_result(article):
                    self.write_article(article)
            page_number += 1
