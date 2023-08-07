from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.dj import DJ
from app.main import get_token, get_auth_header
import requests 
import json
import os

# example_bp = Blueprint('example_bp', __name__)
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
TOKEN = get_token()
AUTH_HEADER = get_auth_header(TOKEN)

dj_bp = Blueprint("dj_bp", __name__, url_prefix="")

@dj_bp.route("/hello")
def hello_world():
    return "<p>Hello World!</p>"


# user_bp.route("/start", methods="GET")
# def get_artist(TOKEN):
    