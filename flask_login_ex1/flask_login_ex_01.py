# Ref: https://www.youtube.com/watch?v=2dEM-s3mRLE

from flask import Flask
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['SECRET_KEY'] = 'asecretkey'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):

    # (per video) Importing the UserMixin provides the 4 methods listed in https://flask-login.readthedocs.io/en/latest/
    # specifically the get_id() that requires id to exists
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)

@login_manager.user_loader
def load_user(user_id):
    # return User.get(user_id)  ## this is per https://flask-login.readthedocs.io/en/latest/, that we have to create...
    print(f'load_user type {type({user_id})} and value {user_id}')  # <class 'set'> and value 1
    user_object = User.query.get(int(user_id))
    print(f'user_object type {type(user_object)} and value {user_object}')  # <class '__main__.User'> and value <User 1>
    return User.query.get(int(user_id))  # Returns the whole user object, which in our case has just a username
    # Note: Per the above link "It should return None (not raise an exception) if the ID is not valid."

#=== ROUTES: ====

@app.route('/')
def index():
    user = User.query.filter_by(username='gideon1').first()  # .first returns teh first result
    print(f'index user type {type(user)} and value: {user}')
    login_user(user)
    return 'You are now logged in.'



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are logged out.'

@app.route('/home')
@login_required
def home():
    return f'The current user is {current_user.username}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
