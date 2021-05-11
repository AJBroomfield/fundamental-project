from application import app, db
from application.models import Character, DiceRoll
from flask import render_template, request, redirect, url_for
from application.forms import CharacterForm, DiceRollForm

@app.route('/')
@app.route('/home')
def home():
    all_characters = Character.query.all()
    all_rolls = DiceRoll.query.all()
    return render_template("index.html", title="Home", all_characters=all_characters, all_rolls=all_rolls)    

@app.route('/addcharacter', methods=["GET","POST"])
def addchar():
    form = CharacterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_char = Character(name=form.name.data, level=form.level.data, race=form.race.data)
            db.session.add(new_char)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template("addchar.html", title='Add a character', form=form)

@app.route('/adddiceroll', methods=["GET","POST"])
def adddice():
    form = DiceRollForm()
    all_characters = Character.query.all()
    for char in all_characters:
        form.character.choices.append((char.id, char.name))
    if request.method == 'POST':
        if form.validate_on_submit():
            new_roll = DiceRoll(
                character_id = form.character.data, 
                dice_num = form.dice_roll.data, 
                dice_result = form.dice_result.data)

            db.session.add(new_roll)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template("adddice.html", title='Add a dice roll', form=form)

# @app.route('/update/<int:id>', methods=["GET","POST"])
# def update(id):
#     task = Tasks.query.filter_by(id=id).first()
#     form = TaskForm()
#     if request.method == "POST":
#         task.desc = form.desc.data
#         db.session.commit()
#         return redirect(url_for('home'))
#     return render_template("edit.html", form=form, title="Update Task", task=task)

# @app.route('/delete/<int:id>', methods=["GET","POST"])
# def delete(id):
#     task = Tasks.query.filter_by(id=id).first()
#     db.session.delete(task)
#     db.session.commit()
#     return redirect(url_for('home'))
    
# @app.route('/complete/<int:id>', methods=["GET","POST"])
# def complete(id):
#     task = Tasks.query.filter_by(id=id).first()
#     task.status = True
#     db.session.commit()
#     return redirect(url_for('home'))

# @app.route('/incomplete/<int:id>')
# def incomplete(id):
#     task = Tasks.query.filter_by(id=id).first()
#     task.status = False
#     db.session.commit()
#     return redirect(url_for('home'))

