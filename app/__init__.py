from flask import Flask, request, jsonify, make_response, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
import base64
import requests
import json
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI")

    # Import models here for Alembic setup
    # from app.models.ExampleModel import ExampleModel
    from .models.user import User

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    # from .routes import example_bp
    # app.register_blueprint(example_bp)
    from app.routes import user_bp
    app.register_blueprint(user_bp)

    @app.route("/hello")
    def hello_world():
        return "<p>Hello World!</p>"
    
    @app.route("/start", methods=["GET"])
    def get_initial_token():
        auth_string = client_id + ":" + client_secret
        auth_bytes = auth_string.encode("utf-8")
        auth_base64= str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization" : "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        result = requests.post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        token = json_result["access_token"]

        print(token)
        return token
    
    #is there a way to store the token in the .env now? if not..
    def get_auth_header(token):
        return {"Authorization" : "Bearer " + token}
    
    @app.route("/start", methods=["POST"])
    # cross origin allow headers OR supports credentials
    def get_track_question():
        # POTENTIAL PARAMETERS: token, limit, market, danceability, max_mode, popularity, valence, artist_seeds = None, track_seeds = None, genre_seeds = None
        # SAMPLE URL: 'https://api.spotify.com/v1/recommendations?limit=1&market=US&seed_artists=4NHQUGzhtTLFvgF5SZesLK&seed_genres=classical%2Ccountry&seed_tracks=0c6xIDDpzE81m2q797ordA&target_danceability=0.8&max_mode=1&target_popularity=70&target_valence=68'
        request_body = request.get_json()
        token = request_body["token"]
        limit = request_body["limit"]
        market = request_body["market"]
        artist_seeds = request_body["artist_seeds"]
        genre_seeds = request_body["genre_seeds"]
        track_seeds = request_body["track_seeds"]
        danceability = request_body["danceability"]
        max_mode = request_body["max_mode"]
        popularity = request_body["popularity"]
        valence = request_body["valence"]

        url = "https://api.spotify.com/v1/recommendations"
        headers = get_auth_header(token)
        params = f"?limit={limit}&market={market}&seed_artists={artist_seeds}&seed_genres={genre_seeds}&seed_tracks={track_seeds}&target_danceability={danceability}&max_mode={max_mode}&target_popularity={popularity}&target_valence={valence}"
        query_url = url + params
        result = requests.get(query_url, headers=headers)
        json_result = json.loads(result.content)
        artist = json_result["tracks"][0]["artists"][0]["name"]
        song_title = json_result["tracks"][0]["name"]
        song_id = json_result["tracks"][0]["id"]
        song_preview = json_result["tracks"][0]["preview_url"]
        #could put token in post request body OR as a cookie. 
        response = {
            "artist": artist,
            "song title": song_title,
            "song_id": song_id,
            "song_preview": song_preview
        }
        return response, 200



    CORS(app)
    return app
