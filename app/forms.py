from flask_sqlalchemy import sqlalchemy
from flask_wtf import Form
from wtforms import StringField, TextField, BooleanField, IntegerField, TextAreaField, SelectMultipleField, SelectField
from wtforms.fields import *
from wtforms import widgets, Form as _Form
#from wtforms.fields.html5 import DataField #gives cannot import DataField error
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from .models import User, Book, Author

class AuthorForm(Form):
    name = TextField('name', validators=[DataRequired()])
    surname = TextField('surname', validators=[DataRequired()])

class UserForm(Form):
    username = TextField('username', validators=[DataRequired()])
    password = TextField('password', validators=[DataRequired()])
    try:
        choices = [(b.title) for b in Book.query.order_by('title')]
    except sqlalchemy.exc.OperationalError as e:
        choices=[]
    books = SelectMultipleField('books', coerce=str, choices=choices)

class BookForm(Form):
    title = TextField('title', validators=[DataRequired()])
    try:
        us = [(u.userid, u.username) for u in User.query.order_by('username')]
    except sqlalchemy.exc.OperationalError as e:
        us=[]
    users =  SelectMultipleField('users', coerce=int ,choices = us)
    try:
        authors = [(a.id, a.name+ " "+ a.surname) for a in Author.query.order_by('surname')]
    except sqlalchemy.exc.OperationalError as e:
        authors=[]
    author = SelectField('bookauthor', coerce=int, choices=authors)

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    remember = BooleanField('remember me')

class IdeaForm(Form):
    idea = TextAreaField('idea', validators=[DataRequired()])


#might have to change forms to later use AJAX in the application - do models first
#class UserForm(Form):
#	name = TextField('title', validators=[DataRequired()])
#	email = TextField('describe', validators=[DataRequired()])
#	phone = IntegerField('describe', validators=[DataRequired()])
#	group = BooleanField('complete'); #should state False at the beginning
