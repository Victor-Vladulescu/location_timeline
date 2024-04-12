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

# base URL
baseUrl = "/timeline_api"

# endpoint routing
api.add_resource(RootEndpoint, baseUrl + "/")
api.add_resource(UpdateLocation_GM, baseUrl + "/update_gm")
