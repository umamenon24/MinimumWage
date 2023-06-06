# flask --app data_server run
from flask import Flask
from flask import render_template
from flask import request
import json
import sys

app = Flask(__name__, static_url_path='', static_folder='static')

states = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Puerto Rico','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont', 'Virginia','Washington','West Virginia','Wisconsin','Wyoming']

@app.route("/")
@app.route('/about')
def about():
    return render_template('about.html', states=states)


@app.route("/macro")
def macro():
    return render_template('macro.html', states=states)

# @app.route("/micro/<state>")
# def micro(state):
#     return render_template('micro.html', state=state)

@app.route("/micro/<state>")
def micro(state):
    return render_template('micro.html', state=state,states=states)

app.run(debug=True)
