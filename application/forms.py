from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired


class CharacterForm(FlaskForm):
    name = StringField('Character Name', validators=[DataRequired()])
    level = IntegerField('Level')
    race = StringField('Character Race', validators=[DataRequired()])
    submit = SubmitField('Add Character')

class DiceRollForm(FlaskForm):
    character = SelectField('Character Name', choices=[])
    dice_roll = SelectField('Dice Rolled', choices=[(4, 'd4'),(6,'d6'),(8,'d8'),(10,'d10'),(20,'d20')])
    dice_result = IntegerField('Dice Result')
    submit = SubmitField('Add Roll')
    
