import re
from quintus import Quintus

quintus = Quintus()

url = "https://postman.zendesk.com/api/v2/help_center/en-us/articles.json"


def name_filter(article):
    return not not re.search(r"(.*?)\s*\\u2014\s*Delisted", article["title"])


filters = [name_filter]

quintus.scrape(url, filters=filters)
