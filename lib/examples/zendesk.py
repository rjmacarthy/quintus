from quintus import Quintus, LoaderType

quintus = Quintus()

quintus.load(
    LoaderType.ZENDESK,
    "https://postman.zendesk.com/api/v2/help_center/en-us/articles.json",
)
