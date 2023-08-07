from app import db
from sqlalchemy.dialects.postgresql import ARRAY

class DJ(db.Model):
    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    logged_in = db.Column(db.Boolean, default = False)
    # relational DB stuff 
    user_prefs =  db.Column(db.ARRAY(db.PickleType), nullable = True)
    saved_playlists = db.Column(db.ARRAY(db.PickleType), nullable = True)
    

    