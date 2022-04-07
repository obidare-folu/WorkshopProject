from folusbudget import db


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	email = db.Column(db.String(60), unique=True, nullable=False)
	password = db.Column(db.String(25), nullable=False)
	user_budget = db.relationship('Budget', backref='person', lazy=True)
	income = db.Column(db.Integer, nullable=False, default=0)
	occupation = db.Column(db.String(20))


class Budget(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
	category = db.Column(db.String, default="Luxury", nullable=False)
	percentage = db.Column(db.Integer, nullable=False, default=0)
	amount = db.Column(db.Integer, nullable=False, default=0)
