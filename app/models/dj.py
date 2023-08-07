from app import db
from sqlalchemy.dialects.postgresql import ARRAY

class DJ(db.Model):
    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    logged_in = db.Column(db.Boolean, default = False)
    # relational DB stuff 
    user_prefs =  db.Column(db.PickleType, nullable = True)
    saved_playlists = db.Column(db.ARRAY(db.PickleType), nullable = True)


    def to_dict(self):
        return {
            "id": self.user_id,
            "name": self.name,
            "logged_in": self.logged_in,
            "user_prefs": self.user_prefs,
            "saved_playlists": [{}]
        }
    
    @classmethod
    def initial_prefs_from_dict(cls, preferences):
        user_initial_prefs = {}
        for key, value in preferences.items():
            if key not in user_initial_prefs:
                user_initial_prefs[key] = value

        # {
        # "token": preferences["token"],
        # "limit": preferences["limit"],
        # "market": preferences["market"],
        # "artist_seeds": preferences["artist_seeds"],
        # "genre_seeds" : preferences["genre_seeds"],
        # "track_seeds": preferences["track_seeds"],
        # "danceability": preferences["danceability"],
        # "max_mode" : preferences["max_mode"],
        # "popularity" : preferences["popularity"],
        # "valence" : preferences["valence"]
        # }
        
        return user_initial_prefs

    @classmethod
    def from_dict(cls, user_data):
        return cls(
            name=user_data["name"])
        