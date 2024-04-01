from flask_restful import Resource
import repository

class RootEndpoint(Resource):

    def get(self):
        return {"message": "Useless endpoint"}, 200


class GetUsers(Resource):

    def get(self):
        return {"users": repository.getUsers()}, 200
