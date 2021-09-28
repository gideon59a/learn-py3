# ref: https://www.techiediaries.com/flask-tutorial-templates/
# To test it do the follwing:
#  1.  (pycharm console) python server.py
#  2.  (chrome) http://127.0.0.1:8000/

import os
from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", message="Hello Flask!", contacts=['c1', 'c2', 'c3', 'c4', 'c5']);
    # return render_template("index.html", message="Hello Flask!");  # a more basic example


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)