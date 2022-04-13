from flask import render_template, request, redirect, url_for, session, make_response
from folusbudget import app
from folusbudget.functions import *
from folusbudget.models import *
from folusbudget.forms import RegistrationForm, LoginForm
import time

@app.route("/", methods=['GET', 'POST'])
@app.route("/home")
def home():
	#db.drop_all()
	db.create_all()
	if 'user' in session:
		print("no he aint")
		return redirect(url_for('client', user=session['user']))
	form = LoginForm()
	if request.method == 'POST':
		print("I came here")
		if form.validate_on_submit():
			print("im validated bitch")
			return login(form.email.data, form.password.data)
		print(form.errors)
	return render_template('home.html', form=form)


@app.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
	db.create_all()
	if 'user' in session:
		return redirect(url_for('client', user=session['user']))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data, password=form.password.data)
		return register(user)
	return render_template('register.html', form=form)


@app.route('/<user>', methods=['GET', 'POST'])
def client(user):

	if 'user' in session:
		this_user = User.query.filter_by(username = session['user']).first()
		income = None
		occupation = None
		if this_user.income > 0:
			income = this_user.income
		if this_user.occupation:
			this_user.occupation = occupation

		if request.method == 'GET':
			cookie = make_response(render_template('user.html', username=user, income=income, occupaton=occupation))
			cookie.set_cookie('user', user)
			return cookie

		if income is not None:
			category = request.form['category']
			percentage = request.form['percentage']
		else:
			this_user.income = request.form['income']
			db.session.commit()
			return redirect(url_for('client', user=this_user.username))
		return add_new_budget_category(category, percentage, this_user)

	return redirect(url_for('home'))


@app.route('/budget-list', methods=['GET'])
def budget_list():
	if 'user' in session:
		if request.method == 'GET':
			user = User.query.filter_by(username = session['user']).first()
			budget = user.user_budget
			return render_template('budget_list.html', budget=budget, username=session['user'])

	return redirect(url_for('home'))


@app.route('/edit-budget', methods=['GET', 'POST'])
def edit_budget():
	if 'user' in session:
		if request.method == 'GET':
			return render_template('edit_budget.html')

		percentage = request.form['newpercentage']
		category = request.form['category2']
		return change_budget(category, percentage)

	return redirect(url_for('home'))


@app.route("/logout")
def logout():
	session.pop("user", None)
	return redirect(url_for('home'))


@app.route("/item", methods=['GET', 'POST'])
def print_item():
	if 'user' in session:
		user = User.query.filter_by(username = session['user']).first()
		budgets = user.user_budget
		item = request.form['search']
		for i in budgets:
			if i.category == item:
				flash(f'Amount you can spend on {item} is {i.amount}', "info")
				break
		else:
			flash(f'{item} is not in your budget', 'danger')
		time.sleep(3)
		return redirect(url_for('client', user=session['user']))

	return redirect(url_for('home'))

# @app.route("/setcookie/<user>")
# def set_cookie(user):
# 	cookie = make_response()
