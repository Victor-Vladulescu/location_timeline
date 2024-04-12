from flask_restful import Resource, reqparse
import json
import repository


class RootEndpoint(Resource):

    def get(self):
        return {"message": "Useless endpoint"}, 200

class UpdateLocation_GM(Resource):

    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('data', type=str, required=True)
        args = parser.parse_args()
        data = args['data']

        # preprocess the data
        data = json.loads(data[4:])

        # extract entries from just the person of interest
        users = []
        for i in data[0]:

            user = {}

            # can we at least get obligatory data?
            try:
                user = {
                    "name": i[0][3],
                    "latitude": i[1][1][2],
                    "longitude": i[1][1][1],
                    "ping": i[1][2] // 1000  # from milliseconds to seconds
                }
            except (Exception):
                continue

            # can we also get this optional info?
            try:
                user["accuracy"] = float(i[1][3])  # not entirely sure, but it should be meters
            except Exception:
                user["accuracy"] = None

            try:
                user["battery"] = i[13][1]
            except Exception:
                user["battery"] = None

            try:
                user["charging"] = bool(i[13][0])
            except Exception:
                user["charging"] = None

            users.append(user)

        if repository.updateLocation_GM(users):
            return {}, 200
        else:
            print("ERROR from repository.updateLocation_GM")
            return {}, 500
