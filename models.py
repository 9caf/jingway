from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Users(db.Model):

	__tablename__ = 'Users'
	"""docstring for Users"""
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String)
	role = db.Column(db.String)
	password = db.Column(db.String)

	def __repr__(self):
		return '<Users %r>' % self.username
		