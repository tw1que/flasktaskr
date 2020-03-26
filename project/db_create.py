import sqlite3
from _config import DATABASE_PATH


with sqlite3.connect(DATABASE_PATH) as connection:

	# create cursor object to execyte SQL commands
	cursor = connection.cursor()

	# create table
	cursor.execute("""CREATE TABLE tasks (
						task_id INTEGER PRIMARY KEY AUTOINCREMENT, 
						name TEXT NOT NULL, 
						due_date TEXT NOT NULL, 
						priority INTEGER NOT NULL,
						status INTEGER NOT NULL
						)""")

	# insert mock data
	cursor.execute("""INSERT INTO tasks (name, due_date, priority, status)
						VALUES ("Finish this course", "01/05/2020", 10, 1)""")

	cursor.execute("""INSERT INTO tasks (name, due_date, priority, status)    
						VALUES ("Finish Real Python Course 2", 
								"01/05/2020", 10, 1)""")
