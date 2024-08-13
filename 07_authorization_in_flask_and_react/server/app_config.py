from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_session import Session
from os import environ
from dotenv import load_dotenv

load_dotenv()

app = Flask(
    __name__,
    static_url_path="",
    static_folder="../client/build",
    template_folder="../client/build",
)


@app.route("/")
@app.route("/productions/new")
@app.route("/productions/<int:id>")
@app.route("/productions/<int:id>/edit")
def index(id=0):
    return render_template("index.html")


# flask-sqlalchemy connection to app
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SESSION_TYPE"] = "sqlalchemy"
db = SQLAlchemy(app)
app.config["SESSION_SQLALCHEMY"] = db

app.secret_key = environ.get("SESSION_SECRET")
# flask-migrate connection to app
migrate = Migrate(app, db)
# flask-restful connection to app
api = Api(app, prefix="/api/v1")
# flask-cors configuration
cors = CORS(app)
# flask-bcrypt configuration
flask_bcrypt = Bcrypt(app)
# flask-session configuration
Session(app)
