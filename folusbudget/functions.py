from folusbudget.models import *
from flask import flash, redirect, url_for, render_template, session


budget_category = dict()


def login(user, password):
	possible_user = User.query.filter_by(username = user).first()
	if possible_user is None:
		possible_user = User.query.filter_by(email = user).first()
	if possible_user is None:
		flash("Invalid username or email address", "danger")
		return redirect(url_for('home'))

	if password == possible_user.password:
		session['user'] = possible_user.username
		return redirect(url_for('client', user=possible_user.username))

	flash("Invalid username or password", "danger")
	return redirect(url_for('home'))

def register(new_user):
	username_exists = User.query.filter_by(username = new_user.username).first()
	email_exists = User.query.filter_by(email = new_user.email).first()
	if username_exists:
		flash("Username already used. Please pick a different username", "danger")
		return redirect(url_for('sign_up'))
	if email_exists:
		flash("Email address already used. Please use another email address", "danger")
		return redirect(url_for('sign_up'))

	db.session.add(new_user)
	db.session.commit()
	luxury = Budget(user=new_user.id, category="Luxury", percentage=0, amount=0)
	db.session.add(luxury)
	db.session.commit()
	flash("You can log in now", 'success')
	return redirect(url_for('home'))



def add_new_budget_category(category, percentag, user):
	if percentag == '' or category == '':
		flash("Fill in all fields", "danger")
		return render_template('user.html', username=user.username)

	percentage = int(percentag)
	if percentage < 1:
		flash("Percentage must be greater than 0", "danger")
		return render_template('user.html', username=user.username)

	budgets = user.user_budget
	luxury = Budget.query.filter_by(category="Luxury", user=user.id).first()
	total_sum = 0
	for i in budgets:
		if i.category == category:
			flash("You already have this category in your budget list. To edit it, go to your budget list and edit")
			return redirect(url_for('client', user=user.username))
		total_sum += i.percentage
	if total_sum + percentage - luxury.percentage > 100:
		flash("This percentage is out of your budget", "danger")
		return render_template('user.html', username=user.username)

	total_sum -= luxury.percentage
	income = user.income
	new_budget = Budget(user=user.id, category=category, percentage=percentage, amount=percentage/100*income)
	total_sum += percentage
	luxury.percentage = 100 - total_sum
	luxury.amount = luxury.percentage/100*income
	db.session.add(new_budget)
	db.session.commit()
	flash("Item has been added to your budget", "info")
	return redirect(url_for('client', user=user.username))


def change_budget(category, percentag):
	if percentag == '' or category == '':
		flash("Fill in all fields", "danger")
		return render_template('edit_budget.html')
	if int(percentag) < 0:
		flash("Percentage cannot be negative", "danger")
		return render_template('edit_budget.html')
	user = User.query.filter_by(username = session['user']).first()
	budgets = user.user_budget
	budget_percentage = 0
	category_exists = False
	budget_id = None
	total_sum = 0
	luxury = None
	for i in budgets:
		if i.category == category:
			category_exists = True
			budget_id = i.id
			budget_percentage = i.percentage
		elif i.category == 'Luxury':
			luxury = i
		else:
			total_sum += i.percentage

	if category_exists:
		if int(percentag) == 0:
			luxury.percentage += budget_percentage
			luxury.amount = luxury.percentage/100*user.income
			Budget.query.filter_by(id=budget_id).delete()
		else:
			budget = Budget.query.get(budget_id)
			budget.percentage = int(percentag)
			budget.amount = budget.percentage/100*user.income
			if total_sum + int(percentag) - luxury.percentage > 100:
				flash("This percentage is out of your budget", "danger")
				return render_template('edit_budget.html')
			else:
				total_sum += int(percentag)
				flash("Your budget has been successfully changed", "info")
				luxury.percentage = 100 - total_sum
				luxury.amount = luxury.percentage/100*user.income
		db.session.commit()
		return redirect(url_for('client', user=user.username))

	flash("This category is not in your budget list", "danger")
	return render_template('edit_budget.html')
