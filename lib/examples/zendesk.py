from quintus import Quintus, LoaderType

quintus = Quintus(
    db_user="postgres",
    db_password="password",
)

quintus.load(
    LoaderType.ZENDESK,
    "https://postman.zendesk.com/api/v2/help_center/en-us/articles.json",
)
