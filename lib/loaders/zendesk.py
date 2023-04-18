import requests
import pydash as _

from loaders.base import Loader


class ZendeskLoader(Loader):
    def __init__(self, url):
        self.name = "zendesk"
        super().__init__(url)

    def get_data(self):
        print("Loading Zendesk data please wait...")
        page_number = 1
        data = []
        while True:
            print(f"Fetching page {page_number}", end="\r")
            response = self.get_page(page_number)
            articles = response["articles"]
            if len(articles) == 0:
                break
            else:
                documents = _.map_(
                    articles,
                    lambda article: {
                        "id": article["id"],
                        "title": article["title"],
                        "body": article["body"],
                        "url": article["html_url"],
                    },
                )
                data.extend(documents)
                page_number += 1
        return data

    def get_page(self, page_number):
        page_url = f"{self.url}?page={page_number}"
        response = requests.get(page_url)
        data = response.json()
        return data
