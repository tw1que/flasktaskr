  ##################
 #### imports #####
##################

from forms import AddTaskForm,RegisterForm, LoginForm

from functools import wraps
import datetime
from flask import Flask, flash, redirect, render_template, \
								request, session, url_for, g
from flask_sqlalchemy import SQLAlchemy


  ################
 #### config ####
################

app = Flask(__name__)
app.config.from_object('_config')
db = SQLAlchemy(app)

from models import Task, User


# helper functions

def login_required(func):
	@wraps(func)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return func(*args, **kwargs)

		else:
			flash('You need to log in first.')
			return redirect(url_for('login'))

	return wrap


  ########################
 #### route handlers ####
########################

@app.route('/logout/')
def logout():
	session.pop('logged_in', None)
	flash('Goodbye!')
	return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
	error = None
	form = LoginForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			user = User.query.filter_by(name=form.name.data).first()
			if user is not None and user.password == form.password.data:
				session['logged_in'] = True
				flash(f'Welcome {form.name.data}!')
				return redirect(url_for('tasks'))
			else:
				error = 'Invalid username or password'
		else:
			error = 'Both fields are required'

	return render_template('login.html', form=form, error=error)

@app.route('/register/', methods=['GET', 'POST'])
def register():
	error = None
	form = RegisterForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			new_user = User(
				form.name.data,
				form.email.data,
				form.password.data,
			)
			db.session.add(new_user)
			db.session.commit()
			flash('Thanks for registering. Please login')
			return redirect(url_for('login'))

	return render_template('register.html', form=form, error=error)

@app.route('/tasks/')
@login_required
def tasks():
	open_tasks = db.session.query(Task).filter_by(status='1') \
					.order_by(Task.due_date.asc())
	closed_tasks = db.session.query(Task).filter_by(status='0') \
					.order_by(Task.due_date.asc())

	return render_template(
		'tasks.html',
		form = AddTaskForm(request.form),
		open_tasks=open_tasks,
		closed_tasks=closed_tasks
		)


#add new task

@app.route('/add/', methods=['GET','POST'])
@login_required
def new_task():

	form = AddTaskForm(request.form)

	if request.method == 'POST':
		if form.validate_on_submit():
			new_task = Task(
				form.name.data,
				form.due_date.data,
				form.priority.data,
				datetime.datetime.utcnow(),
				'1',
				'1'
			)
			db.session.add(new_task)
			db.session.commit()
			flash('New entry was succesfully posted. Thanks.')

	return redirect(url_for('tasks'))

# mark tasks as complete

@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
	new_id = task_id
	db.session.query(Task).filter_by(task_id=new_id).update({'status': '0'})
	db.session.commit()
	flash('The task was marked as comlete. Nice.')

	return redirect(url_for('tasks'))


# delete tasks

@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
	new_id = task_id
	db.session.query(Task).filter_by(task_id=new_id).delete()
	db.session.commit()
	flash('The task was deleted. Why not add another one?')

	return redirect(url_for('tasks'))

