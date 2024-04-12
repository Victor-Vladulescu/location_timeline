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
                    'google_id': u.google_id,
                    'name': u.name,
                    'password': u.password,
                    'last_ping': u.last_ping
                })

            return users

        except:
            return null

def updateLocation_GM(users_location):
    with engine.connect() as conn:
        try:
            query_text = "INSERT INTO public.history (user_id, ping, latitude, longitude, accuracy, battery, charging) VALUES "
            users = getUsers()
            new_pings = []

            for u in users:
                ul = {}

                # TODO use google_id instead of name
                # find current user
                for x in users_location:
                    if u['name'] == x['name']:
                        ul = x
                        break

                # did we even get a user?
                if ul == {}:
                    continue

                # is the "new" ping the same as or older than the old one?
                if ul['ping'] <= u['last_ping']:
                    continue

                # add new ping
                new_pings.append({"user": u['id'], "ping": ul['ping']})

                # add new location
                query_text += f"({u['id']}, {ul['ping']}, {ul['latitude']}, {ul['longitude']},"
                if ul['accuracy']:
                    query_text += f" {ul['accuracy']},"
                else:
                    query_text += " NULL,"

                if ul['battery']:
                    query_text += f" {ul['battery']},"
                else:
                    query_text += " NULL,"

                if ul['charging'] is not None:
                    query_text += f" {ul['charging']}),"
                else:
                    query_text += " NULL),"

            # no new pings?
            if len(new_pings) < 1:
                return True

            # update latest ping for users
            updateLastPing(new_pings)

            # execute SQL query
            query_text = query_text[:-1]
            query_text += ';'
            conn.execute(text(query_text))
            conn.commit()

            return True

        except Exception as ex:
            print("Can't update location_GM")
            print(ex)
            return None


def updateLastPing(pings):
    with engine.connect() as conn:
        try:

            for i in pings:
                conn.execute(text("""UPDATE public.users 
                                     SET last_ping = :ping
                                     WHERE id = :user ;"""), {"ping": i['ping'], "user": i['user']})
                conn.commit()

        except Exception as ex:
            print(ex)
            raise ex
