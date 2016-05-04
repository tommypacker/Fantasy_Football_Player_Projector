from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

class Player(db.Model):
	id = db.Column(db.Integer, primary_key=True)