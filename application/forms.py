from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange, ValidationError, Length


class CheckLevelValue:
    def __init__(self, message="Value isn't an integer"):
        self.message = message
    def __call__(self, form, field):
        if not type(field.data) == int :
            raise ValidationError(self.message)

class CharacterForm(FlaskForm):
    name = StringField('Character Name', validators=[
        DataRequired(), Length(min=2, max=40, message='Enter a name between %(min)d and %(max)d characters long')])
    level = IntegerField('Level', validators=[DataRequired(),
        CheckLevelValue()])
    race = StringField('Character Race', validators=[
        DataRequired(), Length(min=2, max=40, message='Enter a race between %(min)d and %(max)d characters long')])
    submit = SubmitField('Add Character')

class CheckDiceRoll:
    def __init__(self, message='Result is too large'):
        self.message = message
    def __call__(self, form, field):
        if not (field.data <= int(form.dice_roll.data)):
            raise ValidationError(self.message)


class DiceRollForm(FlaskForm):
    character = SelectField('Character Name', choices=[])
    dice_roll = SelectField('Dice Rolled', choices=[(4, 'd4'),(6,'d6'),(8,'d8'),(10,'d10'),(20,'d20')])
    dice_result = IntegerField('Dice Result', validators=[
        DataRequired(), 
        CheckDiceRoll()
    ])
    submit = SubmitField('Add Roll')
    

class UpdateCharacterForm(CharacterForm):
    submit = SubmitField('Update Character')
    
