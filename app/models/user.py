from app import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    logged_in = db.Column(db.Boolean)
    pref_genres = db.Column(db.String)
    name = db.Column(db.String)
    

    