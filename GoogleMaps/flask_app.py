from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, Float, Column, ForeignKey, String
from db_setup import Dealers

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

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        #trial = Trial.query.all()
        #return render_template("stroop.html")
        return render_template("main_page.html", results=Dealers.query.all())
    else:
        name = str(request.form["name"])
        pcode = str(request.form["pcode"])
        cardealer = Dealers(name=name, pcode=pcode)
        db.session.add(cardealer)
        db.session.commit()
        return redirect(url_for('index'))
