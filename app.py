from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.environ["DATABASE_URL"]
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(128))


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    class_year = db.Column(db.Integer)
    role = db.Column(db.String(128))
    linkedin_url = db.Column(db.String(128))


@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route("/projects", methods=["Post"])
def projects():
    # get the request body
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        json = request.get_json()
        name = json["name"]
        description = json["description"]
    else:
        # if there is an error (no request body provided, send a 404 response back)
        return "Bad Request: JSON data with 'name' and 'description' is required.", 404

    # use sqlalchemy to insert a new row into Projects table of the db
    new_project = Projects(name=name, description=description)
    db.session.add(new_project)
    db.session.commit()

    # send a 200 OK response back to the user
    return "Project successfully created!", 200


@app.route("/users", methods=["Post"])
def users():
    # get the request body
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        json = request.get_json()
        name = json["name"]
        class_year = json["class_year"]
        role = json["role"]
        linkedin_url = json["linkedin_url"]
    else:
        return (
            "Bad Request: JSON data with 'name', 'class year', 'role', and 'linkedin_url' is required.",
            404,
        )

    new_user = Users(
        name=name, class_year=class_year, role=role, linkedin_url=linkedin_url
    )
    db.session.add(new_user)
    db.session.commit()

    return "User successfully created!", 200


@app.route("/projects")  # by default, method is get
def getProjects():
    projects = db.session.query(Projects).order_by(Projects.id).all()
    result = []
    for proj in projects:
        print(f"id:{proj.id}")
        proj_dict = {"id": proj.id, "name": proj.name, "description": proj.description}
        result.append(proj_dict)

    return jsonify(result), 200


@app.route("/users")  # by default, method is get
def getUsers():
    users = db.session.query(Users).all()
    result = []
    for use in users:
        use_dict = {
            "id": use.id,
            "name": use.name,
            "class_year": use.class_year,
            "role": use.role,
            "linkedin_url": use.linkedin_url,
        }
        result.append(use_dict)

    return jsonify(result), 200


@app.route("/projects/<id>", methods=["Delete"])
def deleteProject(id):
    try:
        project = db.session.query(Projects).get(id)
        db.session.delete(project)
        db.session.commit()
    except Exception as e:
        print(e)
        return (
            jsonify({"error": "Error deleting project"}),
            500,
        )  # 500 means server error

    return "Project successfully deleted!", 200


@app.route("/users/<id>", methods=["Delete"])
def deleteUsers(id):
    try:
        user = db.session.query(Users).get(id)
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"error": "Error deleting user"}), 500

    return "User successfully deleted!", 200


def partialUpdate(json, databaseObject):
    for data in json:
        if json[data] is not None:
            setattr(databaseObject, data, json[data])


@app.route("/projects/<id>", methods=["Patch"])
def updateProject(id):
    # get the body
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        json = request.get_json()
    else:
        # if there is an error (no request body provided, send a 404 response back)
        return "Updating Eror for projects", 404

    # update the project in the Projects table by the id in the url parameter
    project = db.session.query(Projects).get(id)
    partialUpdate(json, project)
    db.session.commit()
    return "Project Successfully Updated", 200


@app.route("/users/<id>", methods=["Patch"])
def updateUsers(id):
    # get the request body
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        json = request.get_json()
    else:
        return "Updating Erorr for users", 404

    # update the user in the Users table by the id in the url parameter
    user = db.session.query(Users).get(id)
    partialUpdate(json, user)
    db.session.commit()

    # return 200 OK and a helpful message
    return "User Successfully Updated", 200


if __name__ == "__main__":
    app.run(host="localhost", port=8000)
