#!/usr/bin/env python3

#! 📚 Review With Students:
# API Fundamentals
# MVC Architecture and Patterns / Best Practices
# RESTful Routing
# Serialization
# Postman

#! Set Up When starting from scratch:
# In Terminal, `cd` into `server` and run the following:
# export FLASK_APP=app.py
# export FLASK_RUN_PORT=5555
# flask db init
# flask db migrate -m 'Create tables'
# flask db upgrade
# python seed.py


from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Production, CrewMember
from werkzeug.exceptions import NotFound
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///theater.db"

#! Ideal configuration for all your apps
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#! Set up the connection between app and db for alembic - MIGRATION VERSION CONTROL
migrate = Migrate(app, db)
#! Set up the connection between app and db for SQLAlchemy
db.init_app(app)
#! Set up Flask-Restful's Api
api = Api(app, prefix="/api/v1")

@app.route("/")
def homepage():
    return "Hello World!"

# @app.route("/productions", methods=["GET", "POST"])
# def productions():
#     if request.method == "GET":
#         try:
#             #! return a list of dictionaries representing the productions
#             #! INSTEAD OF A LIST OF Production objects WHICH IS NOT serializable
#             prods = [prod.as_dict() for prod in Production.query.all()]

#             # * make_response is the most flexible and explicit of the ways to create a response
#             # return make_response(prods, 200, {"Content-Type": "application/json"})

#             #! jsonify is invoked under the hood automatically
#             # return jsonify(prods), 200

#             #! The following line leverages the fact that Flask will implicitly create a Response object
#             #! jsonify the data and set it as the body of the response object
#             return prods, 200


#         except Exception as e:
#             return {"error": str(e)}, 400
#     else:
#         try:
#             data = request.get_json() #! you might get a 405 if content type has not been set
#             prod = Production(**data) #! model validations kick in at this point
#             db.session.add(prod)
#             db.session.commit() #! database constraints kick in
#             return prod.as_dict(), 201
#         except Exception as e:
#             db.session.rollback()
#             return {"error": e.description}, 400

@app.errorhandler(NotFound)
def page_not_found(error):
    return "This page does not exist", 404


class Productions(Resource):
    def get(self):
        try:
            serialized_prods = [prod.to_dict() for prod in Production.query]
            return make_response(serialized_prods, 200)
            # return serialized_prods, 200
        except Exception as e:
            return {"error": str(e)}
    
    def post(self):
        try:
            data = request.get_json() #! you might get a 405 if content type has not been set
            prod = Production(**data) #! model validations kick in at this point
            db.session.add(prod)
            db.session.commit() #! database constraints kick in
            return prod.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": e.description}, 400

class ProductionByID(Resource):
    def get(self, id):
        try:

            # prod = db.session.get(Production, id)
            if prod := Production.query.get(id):
                return prod.to_dict(rules=("crew_members",)), 200
            return {"error": f"Could not find a Production with id #{id}"}, 404
        except Exception as e:
            return {"error": str(e)}

api.add_resource(Productions, "/productions")
api.add_resource(ProductionByID, "/productions/<int:id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)