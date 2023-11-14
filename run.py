from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://appdev:4W9w5paZIpXv8Gw8LfhmhHAoh811Q8rL@dpg-cl8a0uavokcc73ate250-a.oregon-postgres.render.com/db_lgx2'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(128))
    more = db.Column(db.String(128))

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    app.run(host="localhost", port=8000)
