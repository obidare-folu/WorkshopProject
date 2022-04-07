from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///folusbudget.db'
app.secret_key = 'memyselfandI'

db = SQLAlchemy(app)



from folusbudget import routes
