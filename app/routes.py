from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.dj import DJ
from app.main import get_token, get_auth_header
import requests 
import json
import os, base64

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
TOKEN = get_token()
AUTH_HEADER = get_auth_header(TOKEN)

dj_bp = Blueprint("dj_bp", __name__, url_prefix="")

@dj_bp.route("/hello")
def hello_world():
    return "<p>Hello World!</p>"

@dj_bp.route("/start1", methods =["POST"])
def create_new_user():
    request_body = request.get_json()
    if "name" not in request_body: 
        return ({"details": "Invalid data"}, 400)
    new_user = DJ.from_dict(request_body)

    db.session.add(new_user)
    db.session.commit()
    return make_response({"DJ": new_user.to_dict()}, 201)

@dj_bp.route("/start1", methods=["GET"])
def get_all_DJs():
    response = []
    all_DJs = DJ.query.all()

    for dj in all_DJs:
        response.append(dj.to_dict())
    return jsonify(response), 200


@dj_bp.route("/start1/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = validate_user(DJ, user_id)
    db.session.delete(user)
    db.session.commit()
    return make_response({"details": f"DJ with user ID {user.user_id} and name \"{user.name}\" successfully deleted"}, 200)


# @dj_bp.route("/start1", methods=["GET"])
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

@dj_bp.route("start1/<user_id>", methods=["GET"])
def get_one_dj(user_id):
    user = validate_user(DJ, user_id)
    return make_response({"DJ": user.to_dict()}, 200)

@dj_bp.route("/start1/<user_id>", methods=["PATCH"])
    # cross origin allow headers OR supports credentials
def get_track_question(user_id):
    # POTENTIAL PARAMETERS: token, limit, market, danceability, max_mode, popularity, valence, artist_seeds = None, track_seeds = None, genre_seeds = None
    # SAMPLE URL: 'https://api.spotify.com/v1/recommendations?limit=1&market=US&seed_artists=4NHQUGzhtTLFvgF5SZesLK&seed_genres=classical%2Ccountry&seed_tracks=0c6xIDDpzE81m2q797ordA&target_danceability=0.8&max_mode=1&target_popularity=70&target_valence=68'
    user = validate_user(DJ, user_id)
    preferences = request.get_json()
    # print(preferences)
    user_prefs = DJ.initial_prefs_from_dict(preferences)
    user.user_prefs=user_prefs
    db.session.commit()

    # return make_response(jsonify({"DJ": user.to_dict()}), 200)
    if "seed_tracks" not in preferences:
        temp_token = get_initial_token()
        url = "https://api.spotify.com/v1/recommendations"
        headers = get_auth_header(temp_token)
        params="?"
        for key, value in user.user_prefs.items():
            params+= f"{key}={value}&"
        # params = f"?limit={user.user_prefs['limit']}&market={user.user_prefs['market']}&seed_artists={user.user_prefs['artist_seeds']}&seed_genres={user.user_prefs['genre_seeds']}&seed_tracks={user.user_prefs['track_seeds']}&target_danceability={user.user_prefs['danceability']}&max_mode={user.user_prefs['max_mode']}&target_popularity={user.user_prefs['popularity']}&target_valence={user.user_prefs['valence']}"
        query_url = url + params
        print(query_url)
        result = requests.get(query_url, headers=headers)
        json_result = json.loads(result.content)
        print(json_result)
        artist = json_result["tracks"][0]["artists"][0]["name"]
        song_title = json_result["tracks"][0]["name"]
        song_id = json_result["tracks"][0]["id"]
        song_preview = json_result["tracks"][0]["preview_url"]
        photo = json_result["tracks"][0]["album"]["images"][1]
            #could put token in post request body OR as a cookie. 
        response = {
                "artist": artist,
                "song_title": song_title,
                "song_id": song_id,
                "song_preview": song_preview,
                "album_art": photo
            }
        return response, 200
    else: #THIS WILL BE THE PROTOCOL FOR THE SECOND AND FINAL SEARCH 
        temp_token = get_initial_token()
        url = "https://api.spotify.com/v1/recommendations"
        headers = get_auth_header(temp_token)
        # params = f"?limit={10}&market={user.user_prefs['market']}&seed_artists={user.user_prefs['artist_seeds']}&seed_genres={user.user_prefs['genre_seeds']}&seed_tracks={user.user_prefs['track_seeds']}&target_danceability={user.user_prefs['danceability']}&max_mode={user.user_prefs['max_mode']}&target_popularity={user.user_prefs['popularity']}&target_tempo={user.user_prefs['tempo']}&target_valence={user.user_prefs['valence']}"
        params="?"
        for key, value in user.user_prefs.items():
            params+= f"{key}={value}&"
        # audio_features = get_audio_features()
        # for key, value in user.user_prefs.items():
        #     params+= f"{key}={value}&"
        query_url = url + params
        result = requests.get(query_url, headers=headers)
        json_result = json.loads(result.content)
        response = []
        # song_data = {}
        for i in range(10):
            artist = json_result["tracks"][i]["artists"][0]["name"]
            song_title = json_result["tracks"][i]["name"]
            song_id = json_result["tracks"][i]["id"]
            song_preview = json_result["tracks"][i]["preview_url"]
            photo = json_result["tracks"][i]["album"]["images"][1]
            song_data = {
                "artist": artist,
                "song_title": song_title,
                "song_id": song_id,
                "song_preview": song_preview,
                "album_art": photo
            }
            response.append(song_data)
        return jsonify(response), 200
    
def validate_user(model, user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        return abort(make_response({"message": f"invalid id: {user_id}"}, 400))
    return model.query.get_or_404(user_id, description=f"{model.__name__} with id {user_id} not found")

def get_audio_features(song_id, temp_token):
    # temp_token = get_initial_token()
    url = f"https://api.spotify.com/v1/audio-features/{song_id}"
    headers = get_auth_header(temp_token)
    result = requests.get(url, headers=headers)
    json_result = json.loads(result.content)
    print(json_result)
    max_key = json_result["key" + 1]
    min_key = json_result["key" -1]
    min_tempo = json_result["tempo" -10]
    max_tempo = json_result["tempo" + 10]
    target_time_signature = json_result["time_signature"]
    audio_features = {
        "min_key": min_key,
        "max_key" : max_key,
        "min_tempo" : min_tempo,
        "max_tempo": max_tempo,
        "target_time_signture": target_time_signature
    }
    return audio_features
