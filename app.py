from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

with app.app_context():
    db.create_all()

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/list")
def list():    
    todo_list = db.session.query(Todo).all()
    return render_template("list.html", todo_list=todo_list)

@app.get("/todo/<int:todo_id>")
def todo(todo_id):    
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        return f"No Todo item {todo_id} found.", 404
    return render_template("todo.html", todo=todo)

@app.post("/add")
def add():
    title = request.form.get("title", "").strip()
    if not title:
        flash("Title cannot be empty.", "error")
        return redirect(url_for("list"))
    if len(title) > 100:
        flash("Title must be 100 characters or fewer.", "error")
        return redirect(url_for("list"))
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("list"))


@app.post("/update/<int:todo_id>")
def update(todo_id):
    todo = db.get_or_404(Todo, todo_id)
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("list"))


@app.post("/delete/<int:todo_id>")
def delete(todo_id):
    todo = db.get_or_404(Todo, todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("list"))
