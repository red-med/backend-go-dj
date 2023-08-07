from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64= str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token 

def get_auth_header(token):
    return {"Authorization" : "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("no existing artist with this name...")
        return None 
    
    return json_result[0]

def get_top_tracks_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_user_prefs(token):
    # url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    # headers = get_auth_header(token)
    # result = get(url, headers=headers)
    # json_result = json.loads(result.content)
    # return json_result
    pref_genres = input()
    pass 

def get_a_recc(token):
        url = "https://api.spotify.com/v1/recommendations"
        headers = get_auth_header(token)
        limit = 1
        market = "US"
        artist_seeds = "4NHQUGzhtTLFvgF5SZesLK"
        genre_seeds = "hip-hop,r-n-b"
        track_seeds = "0c6xIDDpzE81m2q797ordA"
        danceability = 0.8
        max_mode = 1
        popularity = 70
        valence = 68
        params = f"?limit={limit}&market={market}&seed_artists={artist_seeds}&seed_genres={genre_seeds}&seed_tracks={track_seeds}&target_danceability={danceability}&max_mode={max_mode}&target_popularity={popularity}&target_valence={valence}"
        query_url = url + params
        result = get(query_url, headers=headers)
        json_result = json.loads(result.content)
        return json_result
        # artist = json_result["tracks"]["artists"]["name"]
        # song_title = json_result["tracks"]["name"]
        # song_id = json_result["tracks"]["id"]
        # song_preview = json_result["preview_url"]


# def get_recs(token, genre_seeds = None, track_seeds = None, artist_seeds = None,
#                 )

# token = get_token()
# artist_data = search_for_artist(token, "Kanye West")
# artist_id = artist_data["id"]
# songs = get_top_tracks_by_artist(token, artist_id)

# available_genres = get_genres(token)
# print(available_genres)



# token = get_token()
# recc_data = get_a_recc(token)
# artist = recc_data["tracks"][0]["artists"][0]["name"]
# song_title = recc_data["tracks"][0]["name"]
# song_id = recc_data["tracks"][0]["id"]
# song_preview = recc_data["tracks"][0]["preview_url"]
# print("artist:", artist)
# print("song title:", song_title)
# print("song id: ", song_id)
# print("preview:" , song_preview)

# for index, song in enumerate(songs):
#     print(f"{index + 1 }.{song['name']}")