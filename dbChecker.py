import sqlite3
from os.path import exists

if exists("todos.db") == False:
    open("todos.db", "x")

connection = sqlite3.connect("todos.db")
cursor = connection.cursor()

try:
    cursor.execute("""SELECT * FROM todos; """).fetchall()
    connection.close()
except:
    todosTable = """
    CREATE TABLE "todos" (
	"id"	INTEGER,
    "todo"	TEXT,
    "date"	TEXT,
    "time"	TEXT,
    "status"	TEXT DEFAULT 'False',
    "editDate"	TEXT,
    "editTime"	INTEGER,
    PRIMARY KEY("id" AUTOINCREMENT)
    );"""
    cursor.execute(todosTable)
    connection.commit()
    connection.close()
