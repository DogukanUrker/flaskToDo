import socket
import sqlite3
import secrets
import dbChecker
from datetime import datetime
from flask import Flask, render_template, redirect

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)


def currentDate():
    return datetime.now().strftime("%d.%m.%y")


def currentTime():
    return datetime.now().strftime("%H:%M")


@app.route("/")
def index():
    connection = sqlite3.connect("todos.db")
    cursor = connection.cursor()
    cursor.execute("select * from todos")
    todos = cursor.fetchall()
    return render_template("/index.html", todos=todos)


@app.route("/add/<todo>")
def add(todo):
    connection = sqlite3.connect("todos.db")
    cursor = connection.cursor()
    cursor.execute(
        f'insert into todos(todo,date,time) values("{todo}","{currentDate()}","{currentTime()}")'
    )
    connection.commit()
    return redirect("/")


@app.route("/check/<int:id>")
def check(id):
    connection = sqlite3.connect("todos.db")
    cursor = connection.cursor()
    cursor.execute(f'update todos set status = "True" where id = {id}')
    cursor.execute(f'update todos set editDate = "{currentDate()}" where id = {id}')
    cursor.execute(f'update todos set editTime = "{currentTime()}" where id = {id}')
    connection.commit()
    return redirect("/")


@app.route("/uncheck/<int:id>")
def uncheck(id):
    connection = sqlite3.connect("todos.db")
    cursor = connection.cursor()
    cursor.execute(f'update todos set status = "False" where id = {id}')
    connection.commit()
    return redirect("/")


@app.route("/edit/<int:id>/<todo>")
def edit(id, todo):
    connection = sqlite3.connect("todos.db")
    cursor = connection.cursor()
    cursor.execute(f'update todos set todo = "{todo}" where id = {id}')
    connection.commit()
    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):
    connection = sqlite3.connect("todos.db")
    cursor = connection.cursor()
    cursor.execute(f"delete from todos where id = {id}")
    cursor.execute(f"update sqlite_sequence set seq = seq-1")
    connection.commit()
    return redirect("/")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(
        debug=True,
        host=socket.gethostbyname(socket.gethostname()),
    )
