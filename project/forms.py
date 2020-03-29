from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, \
					SelectField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class AddTaskForm(Form):

	# task_id = IntegerField() # >> Redundant?
	name = StringField(
		'Task Name', 
		validators=[DataRequired()]
		)
	due_date = DateField(
		'Date Due (mm/dd/yyyy)',
		validators=[DataRequired()], format='%m/%d/%Y'
		)
	priority = SelectField( # >> Redundant?
		'Priority',
		validators=[DataRequired()],
		choices=[
			('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
			('6', '6'), ('6', '6'), ('8', '8'), ('9', '9'), ('10',' 10')
			]
		)
	status = IntegerField('Status')


class RegisterForm(Form):

	name = StringField(
		'Username',
		validators=[DataRequired(), Length(min=6, max=25)]
	)
	email = StringField(
		'Email',
		validators=[DataRequired(), Email(), Length(min=6, max=40)]
	)
	password = PasswordField(
		'Password',
		validators=[DataRequired(), Length(min=6, max=40)]
	)
	confirm = PasswordField(
		'Repeat password',
		validators=[
			DataRequired(), 
			EqualTo('password', message='Passwords must match')
		]
	)

class LoginForm(Form):

	name = StringField(
		'Username',
		validators=[DataRequired()]
	)
	password = PasswordField(
		'Password',
		validators=[DataRequired()]
	)




