from application import app, db
from application.models import Character, DiceRoll
from flask import render_template, request, redirect, url_for
from application.forms import CharacterForm, DiceRollForm

@app.route('/')
@app.route('/home')
def home():
    all_characters = Character.query.all()
    all_rolls = DiceRoll.query.all()
    output = ""
    return render_template("index.html", title="Home", all_characters=all_characters, all_rolls=all_rolls)    

# @app.route('/create', methods=["GET","POST"])
# def create():
#     form = TaskForm()
#     if request.method == 'POST':
#         if form.validate_on_submit():
#             new_task = Tasks(desc=form.desc.data)
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect(url_for('home'))
#     return render_template("add.html", title='Create a task', form=form)

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

