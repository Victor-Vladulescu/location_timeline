from sqlalchemy import text
from singletons import *


def getUsers():
    with engine.connect() as conn:
        try:
            query = conn.execute(text("""SELECT * FROM public.users"""))

            users = []

            for u in query:
                users.append({
                    'id': u.id,
                    'name': u.name,
                    'last_ping': u.last_ping
                })

            return users

        except:
            return null