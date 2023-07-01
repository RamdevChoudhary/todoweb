#-------------------------------------Overview-------------------------------------#
# This code implements a basic Todo application using Flask, SQLAlchemy, and SQLite.
# The application allows users to add, update, and delete tasks in a todo list. The 
# tasks are stored in a SQLite database using SQLAlchemy as an ORM 
# (Object-Relational Mapping) tool.

# **Dependencies
# The following libraries are required to run the code:#

                 # **Flask** #
              # **SQLAlchemy** #

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# Flask: The Flask library is imported to create the Flask application instance.
# render_template: This function is imported to render HTML templates.
# request: This module is imported to handle HTTP requests.
# redirect: This function is imported to redirect the user to a different URL.
# Flask_SQLAlchemy: This extension is imported to connect the Flask application with the SQLite database.
# datetime: This module is imported to handle timestamps for the tasks.

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tudo.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    ### Database Model ###
    # The database model is defined using SQLAlchemy in the following class:
    
    def __repr__(self) -> str:
        return f"{self.sno}  -  {self.title}"

# Routes and Functionality
# Route: "/"
# This route handles the home page and allows users to add new tasks and 
# view existing tasks.
@app.route("/", methods=['GET', 'POST'])
def helloworld():
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template("index.html", allTodo = allTodo)

@app.route("/show")
def products():
    allTodo = Todo.query.all()
    return "this is a product page"

@app.route("/update/<int:sno>",  methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=8000)


