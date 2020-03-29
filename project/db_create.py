from views import db
from models import Task
from datetime import date

db.create_all()

# db.session.add(Task('Finish this tutorial', date(2020, 1, 5), 10, 1))
# db.session.add(Task('Finish Real Python', date(2020, 1, 6), 10, 1))

db.session.commit()