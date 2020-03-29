from views import db
from _config import DATABASE_PATH

import sqlite3
from datetime import datetime

with sqlite3.connect(DATABASE_PATH) as connection:

	# get cursor object for executing SQL commands
	cursor = connection.cursor()

	# temporarliy change the name of the tasks table
	cursor.execute("""ALTER TABLE tasks RENAME TO old_tasks""")

	# recreate a new tasks table with the updated schema
	db.create_all()

	# retrieve data from the old_tasks table
	cursor.execute("""SELECT name, due_date, priority, status
						FROM old_tasks ORDER BY task_id ASC""")

	# save all rows as a list of tuples; set posted_date and user_id to 1
	data = [
		(row[0], row[1], row[2], row[3], datetime.now(), 1) 
		for row in cursor.fetchall()
	]

	# insert data into the new tasks table
	cursor.executemany("""INSERT INTO tasks (name, due_date, 
							priority, status, posted_date, user_id)
							VALUES (?,?,?,?,?,?)""", 
							data
						)

	# delete the old tasks table
	cursor.execute("""DROP TABLE old_tasks""")