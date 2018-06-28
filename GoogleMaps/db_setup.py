from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, Float, Column, ForeignKey, String

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="DennisDemenis",
    password="advanced",
    hostname="DennisDemenis.mysql.pythonanywhere-services.com",
    databasename="DennisDemenis$cardealers",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Dealers(db.Model):
    __tablename__ = "dealers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(String(128))
    pcode = db.Column(String(128))

# RUN OUTSIDE OF THE SCRIPT:
#from db_setup import db
#db.create_all()
