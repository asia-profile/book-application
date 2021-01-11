from app import db

usersbooks = db.Table('usersbooks', db.Model.metadata,
	db.Column('userid', db.Integer, db.ForeignKey('user.userid')),
	db.Column('title', db.String, db.ForeignKey('book.title')))


class Author(db.Model):
	id = db.Column(db.Integer, primary_key=True) #our primary key
	name = db.Column(db.String(200), index=True, unique=True)
	surname = db.Column(db.String(200), index=True, unique=True)
	books = db.relationship('Book', backref='author', lazy="dynamic")

	def __repr__(self):
		return self.name + " " + self.surname


class User(db.Model):
	userid = db.Column(db.Integer, primary_key=True) #our primary key
	username = db.Column(db.String(200), index=True, unique=True)
	password = db.Column(db.String(200), index=True, unique=True)
	books=db.relationship('Book',secondary=usersbooks)

	def __repr__(self):
		return self.username

class Book(db.Model):
	title = db.Column(db.String(200), index=True, primary_key=True) #our primary key here
	users = db.relationship('User', secondary=usersbooks)
	bookauthor = db.Column(db.Integer, db.ForeignKey('author.id')) #changed from simply author, got tid of one error creating backref

class Idea(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(500), index=True, unique=True)


	def __repr__(self):
		return self.title
