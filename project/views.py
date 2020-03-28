import sqlite3
from functools import wraps

from flask import Flask, flash, redirect, render_template, \
								request, session, url_for, g
from forms import AddTaskForm


# config
app = Flask(__name__)
app.config.from_object('_config')


# helper functions
def connect_db():
	return sqlite3.connect(app.config['DATABASE_PATH'])


def login_required(func):
	@wraps(func)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return func(*args, **kwargs)

		else:
			flash('You need to log in first.')
			return redirect(url_for('login'))

	return wrap


# route handlers
@app.route('/logout/')
def logout():
	session.pop('logged_in', None)
	flash('Goodbye!')
	return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
	if request.method=='POST':
		if request.form['username'] != app.config['USERNAME'] or \
			request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid Credentials. Please try again'
			return render_template('login.html', error=error)
		else:
			session['logged_in'] = True
			flash('Welcome!')
			return redirect(url_for('tasks'))

	return render_template('login.html')


@app.route('/tasks/')
@login_required
def tasks():
	with connect_db() as g.db:
		cursor = g.db.execute(
			'SELECT name, due_date, priority, task_id FROM tasks WHERE status=1'
			)

		open_tasks = [
			dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3])
				for row in cursor.fetchall()
		]

		cursor = g.db.execute(
			'SELECT name, due_date, priority, task_id FROM tasks WHERE status=0'
			)

		closed_tasks = [
			dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3])
				for row in cursor.fetchall()
		]

	return render_template(
		'tasks.html', 
		form=AddTaskForm(request.form),
		open_tasks=open_tasks,
		closed_tasks=closed_tasks
		)


#add new task
@app.route('/add/', methods=['POST'])
@login_required
def new_task():
	with connect_db() as g.db:

		name = request.form['name']
		date = request.form['due_date']
		priority = request.form['priority']
		if not name or not date or not priority:
			flash('All fields are required. Please try agian.')
			return redirect(url_for('tasks'))
		else:
			g.db.execute('INSERT INTO tasks (name, due_date, priority, \
							status) VALUES (?,?,?,1)', [
												request.form['name'],
												request.form['due_date'],
												request.form['priority']
												]
												)
			flash('New entry was succesfully posted')
	
	return redirect(url_for('tasks'))


# mark tasks as complete
@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
	with connect_db() as g.db:
		g.db.execute('UPDATE tasks SET status = 0 WHERE task_id = ?', 
						(task_id, ))

		flash('The task was marked as comlete.')

	return redirect(url_for('tasks'))


# delete tasks
@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
	with connect_db() as g.db:
		g.db.execute('DELETE FROM tasks WHERE task_id = ?', (task_id, ))

		flash('Task was deleted succesfully')

	return redirect(url_for('tasks'))











