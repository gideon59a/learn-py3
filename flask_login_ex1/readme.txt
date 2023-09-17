There are several examples in this folder:

1. flask-sqlalchemy-example.py - When I run it it creates the flask-sqlalchemy-example sqlite3 db file.

2. flask_login_ex_01.py - A basic example of flask login

3. flask_login_web_form.py - A more comprehensive flask login example, which includes web form to login and access
   Uses the ./templates folder
   Uses login.db (that was created and filled-up at linux level)
   Note that the commnons folder is not really needed (used for the next failed example)

4. py_client_towards_flask_login_web_form.py - using python instead of web to access the server. Failed to access where
   login was required because session was not used. I'll not enhance it further - instead I'll add to
   - a flask-socketio the login capabilities
   - a flask-asyncio client the session capabilities
