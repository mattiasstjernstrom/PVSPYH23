from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+mysqlconnector://root:password@localhost:3306/flask_db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)


def create_user_table():
    with app.app_context():
        db.create_all()

        if not User.query.first():
            seed_data()


def seed_data():
    user = User(name="Mattias Stjernström", email="mail@mehow.se")
    db.session.add(user)
    db.session.commit()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST" and request.args.get("_method") == "delete":
        id = request.form["id"]
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()

    elif request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        user = User(name=name, email=email)

        db.session.add(user)
        db.session.commit()

    users = User.query.all()
    return render_template("index.html", users=users)


@app.route("/uppdatera/<id>", methods=["GET", "POST"])
def uppdatera(id):
    user = User.query.filter_by(id=id).first()
    if request.method == "POST" and request.args.get("_method") == "put":
        name = request.form["name"]
        email = request.form["email"]

        user.name = name
        user.email = email

        db.session.commit()
        return redirect("/")
    return render_template("uppdatera.html", user=user)


if __name__ == "__main__":
    create_user_table()
    app.run(debug=True)
