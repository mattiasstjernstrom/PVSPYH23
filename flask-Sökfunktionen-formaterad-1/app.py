from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, asc, desc
from faker import Faker
from flask_migrate import Migrate

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+mysqlconnector://root:password@localhost:3306/flask_db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)


def create_user_table():
    with app.app_context():
        db.create_all()

        if not User.query.first():
            seed_data()


def seed_data():
    fk = Faker()
    iterations = 0

    while iterations < 20:  # Vi börjar med 20
        user = User(
            name=fk.name(),
            email=fk.email(),
        )
        db.session.add(user)
        db.session.commit()
        iterations += 1


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


@app.route("/sok", methods=["GET"])
def sok():
    page = request.args.get("page", 1, type=int)
    per_page = 5
    input = request.args.get("q") or ""

    users_query = User.query.filter(
        or_(User.name.contains(input), User.email.contains(input))
    )

    sort = request.args.get("sort")

    if sort == "name_asc":
        users_query = users_query.order_by(asc(User.name))
    elif sort == "name_desc":
        users_query = users_query.order_by(desc(User.name))
    elif sort == "email_asc":
        users_query = users_query.order_by(asc(User.email))
    elif sort == "email_desc":
        users_query = users_query.order_by(desc(User.email))

    users_pagination = users_query.paginate(page=page, per_page=per_page)
    users = users_pagination.items

    next_url = (
        url_for("sok", q=input, page=users_pagination.next_num)
        if users_pagination.has_next
        else None
    )
    prev_url = (
        url_for("sok", q=input, page=users_pagination.prev_num)
        if users_pagination.has_prev
        else None
    )

    return render_template(
        "sok.html",
        q=input,
        current_page=page,
        results=users,
        next_url=next_url,
        prev_url=prev_url,
    )


if __name__ == "__main__":
    create_user_table()
    app.run(debug=True)
