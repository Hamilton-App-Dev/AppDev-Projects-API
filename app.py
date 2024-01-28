from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://appdev:4W9w5paZIpXv8Gw8LfhmhHAoh811Q8rL@dpg-cl8a0uavokcc73ate250-a.oregon-postgres.render.com/db_lgx2'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Projects(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(128))

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    class_year = db.Column(db.Integer)
    role = db.Column(db.String(128))
    linkedin_url = db.Column(db.String(128))

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.route('/projects', methods = ['Post'])
def projects():
    # get the request body
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.get_json()
        name = json['name']
        description = json['description']
    else:
        # if there is an error (no request body provided, send a 404 response back)
        return "Bad Request: JSON data with 'name' and 'description' is required.", 404

    # use sqlalchemy to insert a new row into Projects table of the db
    new_project = Projects(name = name, description = description)
    db.session.add(new_project)
    db.session.commit()

    # send a 200 OK response back to the user
    return "Project successfully created!", 200

@app.route('/projects')  # by default, method is get
def getProjects():
    projects = db.session.query(Projects).all()
    result = []
    # in for loop, turn projects class to append to results array,
    # then call:
    # convert into JSON:
         #y = json.dumps(x)

    for proj in projects:
        print(f'Id: {proj.id} Name: {proj.name} Description: {proj.description}')
    return json, 200

@app.route('/projects/{id}', methods=['delete'])  # by default, method is get
def getProjects():

# define the flask route
# @app.route('/projects', methods = 3['Post'])
# 


if __name__ == "__main__":
    app.run(host="localhost", port=8000)
