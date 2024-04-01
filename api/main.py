from flask import Flask, send_from_directory
from flask_restful import Api
from flask_cors import CORS
from controller import *

# app config
app = Flask("Location_timeline")

# allow CORS
CORS(app)

# make api
api = Api(app)

# endpoint routing
api.add_resource(RootEndpoint, "/")
api.add_resource(GetUsers, "/users")

# run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
