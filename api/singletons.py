from sqlalchemy import *
import os

try:
    dbstring = os.environ['DB_timeline']
    engine = create_engine(dbstring, echo=False)
except Exception as e:
    print(e)
    exit()
