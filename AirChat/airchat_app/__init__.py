from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sendgrid import SendGrid

app = Flask(__name__)
app.config['SECRET_KEY']=''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SENDGRID_API_KEY'] = ''
app.config['SENDGRID_DEFAULT_FROM'] = ''

db = SQLAlchemy(app)
mail = SendGrid(app)

from airchat import routes

