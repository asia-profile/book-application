import logging
from flask import render_template, flash, request, redirect, url_for,session, g, make_response
from flask import jsonify
from flask_admin.contrib.sqla import ModelView
from app import app, db, admin #, models
from .models import User, Book, Author, Idea

from .forms import UserForm, BookForm, AuthorForm, LoginForm, IdeaForm

admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Book,db.session))
admin.add_view(ModelView(Author,db.session))

@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie(): #/setcookie
	if not request.cookies.get('cookie'):
		res = make_response(render_template('log.html'))
		res.set_cookie('cookie', 'set', max_age=60*60*24*365*2)
	else:
		res = make_response('Value of cookie is {}' .format(request.cookies.get('cookie')))
	return res
	#if request.method == 'POST':
		#value = request.form['value'#]

	#resp = make_response(render_template('log.html'))
	#resp.set_cookie('variable_name', value)

	#return resp

@app.route('/getcookie')
def getcookie():
   name = request.cookies.get('variable_name')
   return '<h1>Cookie value set to: '+name+'</h1>'


#not 100% sure here
@app.route('/', methods=['GET', 'POST'])
def login():
	app.logger.info('Info level log')
	app.logger.warning('Warning level log')

	form=LoginForm()

	if form.validate_on_submit():
		user=User.query.filter_by(username=form.username.data).first()
		if user:
			if user.password==form.password.data:
				return redirect(url_for('home'))
		return '<h1> Invalid username or password</h1>'

	return render_template('log.html', form=form)



@app.route('/home')
def home():
	return render_template("home.html")

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
	form=UserForm()
	flash('Errors="%s"'%(form.errors))
	if form.validate_on_submit():
		u=User(username=form.username.data, password=form.password.data)
		for title in form.books.data:
			b=Book.query.get(title) #booktitle
			u.books.append(b)
		db.session.add(u)
		db.session.commit()
		return redirect('/users')
	return render_template('create_user.html',
							title='Create User',
							form=form)

@app.route('/create_author', methods=['GET', 'POST'])
def create_author():
	form=AuthorForm()
	flash('Errors="%s"'%(form.errors))
	if form.validate_on_submit():
		a=Author(name=form.name.data, surname=form.surname.data)
		db.session.add(a)
		db.session.commit()
		return redirect('/authors')
	return render_template('create_author.html',
							title='Create Author',
							form=form)

@app.route('/create_book', methods=['GET', 'POST'])
def create_book():
	form=BookForm()
	flash('Errors="%s"'%(form.errors))
	if form.validate_on_submit():
		b=Book(title=form.title.data)
		for userhold in form.users.data:
			user=User.query.get(userhold)
			b.users.append(user)
		author = Author.query.get(form.author.data)
		#print(author)
		b.author=author
		db.session.add(b)
		db.session.commit()
		return redirect('/books')

	return render_template('create_book.html',
							title='Create Book',
							form=form)


@app.route('/delete_user/<userid>', methods=['GET'])
def delete_user(userid):
	user = User.query.get(userid)
	db.session.delete(user)
	db.session.commit()
	return redirect('/users')

@app.route('/delete_author/<id>', methods=['GET'])
def delete_author(id):
	author = Author.query.get(id)
	db.session.delete(author)
	db.session.commit()
	return redirect('/authors')

@app.route('/delete_book/<title>', methods=['GET'])
def delete_book(title):
	book = Book.query.get(title)
	db.session.delete(book)
	db.session.commit()
	return redirect('/books')

@app.route('/users', methods=['GET'])
def getAllUsers():
	users=User.query.all()
	return render_template('user_list.html',
						title='All Users', users=users)

@app.route('/authors', methods=['GET'])
def getAllAuthors():
	authors=Author.query.all()
	return render_template('author_list.html',
						title='All Authors', authors=authors)

@app.route('/books', methods=['GET'])
def getAllBooks():
	books=Book.query.all()
	return render_template('book_list.html',
						title='All Books', books=books)

@app.route('/quiz')
def quiz():
	return render_template('quiz.html')


@app.route('/background_process')
def background_process():
	try:
		lang = request.args.get('proglang', 0, type=str)
		if lang.lower() == 'Szekspir':
			return jsonify(result='You are wise')
		else:
			return jsonify(result='Try again.')
	except Exception as e:
		return str(e)



@app.route('/ideas', methods=['GET', 'POST'])
def ideas():

	form = IdeaForm()
	if form.validate_on_submit():
		# Save idea
		new_idea = Idea(text=form.idea.data)
		db.session.add(new_idea)
		db.session.commit()

		flash("Thanks for your bright new idea: " + str(form.idea.data))

	# Query after having added new idea
	ideas = Idea.query.all()
	print("Number of new ideas in db:", len(ideas))

	return render_template('ideas.html', form=form, ideas=ideas)


@app.route('/books/<id>', methods=['GET'])
def getAllBooksWrittenBy(id):
	author=Author.query.filter_by(id=id).first()
	return render_template('book_list.html',
							title="Books written by"+ str(author),
							books=author.books)

@app.route('/books/users/<userid>', methods=['GET'])
def getAllBooksReadBy(userid):
	user=User.query.filter_by(userid=userid).first()
	return render_template('book_list.html',
							title="Books read by"+ str(user),
							books=user.books)

@app.route('/edit_user/<userid>', methods=['GET','POST'])
def edit_user(userid):
	user=User.query.get(userid)
	form=UserForm(obj=user)
	flash('Erros="%s"'%(form.errors))
	if form.validate_on_submit():
		t=user
		t.username=form.username.data
		t.password=form.password.data
		for title in form.books.data:
			book=Book.query.get(title)
			t.books.append(book)
		db.session.commit()
		return redirect('/users')

	return render_template('edit_user.html',
							title='Edit User', form=form)


#if __name__=="__main__"
	#app.run(debug=True)
