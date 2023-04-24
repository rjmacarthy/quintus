from quintus import Quintus, Provider

quintus = Quintus(
  db_user="postgres",
  db_password="password",
)

quintus.chat(Provider.OPEN_AI)
