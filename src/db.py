import databases
from sqlalchemy import MetaData

from settings import settings

db = databases.Database(settings.DATABASE_URL)
metadata = MetaData()
