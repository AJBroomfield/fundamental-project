from application import db
from datetime import datetime

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    race = db.Column(db.String(40), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rolls = db.relationship('DiceRoll', backref='character')

class DiceRoll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    dice_num = db.Column(db.Integer, nullable=False)
    dice_result = db.Column(db.Integer, nullable=False)