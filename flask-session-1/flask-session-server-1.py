# ref: https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/?ref=rp

from flask import Flask, render_template, redirect, request, session
# The Session instance is not used for direct access, for which you should always use flask.session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"  # One can use other db type, like sqlalchemy, redis, etc. With this the
                                            # server creatres a sub-folder and puts the sessions there.
Session(app)


@app.route("/")
def index():
    if not session.get("name"):
        return redirect("/login")
    return render_template('index.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        print(f'request.form: {request.form}')  # Ex: "request.form: ImmutableMultiDict([
                                                # ('name', 'gideon'), ('Register', 'Submit')])"
                                                # which are the login.html fields sent
        session["name"] = request.form.get("name")
        return redirect("/")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
