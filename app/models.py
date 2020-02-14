from app import db
from datetime import datetime

class Model(db.Model):
	__tablename__ = "model"
	__table_args__ = {'mysql_collate': 'utf8_general_ci'}
	no = db.Column(db.Integer, primary_key=True)	
	title = db.Column(db.String(128))	
	content = db.Column(db.Text)
	date = db.Column(db.DateTime)
	file = db.Column(db.String(256))

	def __init__(self, title, content, date, file):		
		self.title = title
		self.content = content
		self.date = date
		self.file = file

class User(db.Model):
	__tablename__ = "user"
	__table_args__ = {'mysql_collate': 'utf8_general_ci'}
	id = db.Column(db.String(32), primary_key=True)
	pw = db.Column(db.String(64))
	
	def __init__(self, id, pw):
		self.id = id
		self.pw = pw

class Result(db.Model):
	__tablename__ = "result"
	__table_args__ = {'mysql_collate': 'utf8_general_ci'}
	no = db.Column(db.Integer, primary_key=True)
	result = db.Column(db.Integer)
	date = db.Column(db.DateTime)
		
	def __init__(self, result, date):		
		self.result = result
		self.date = date