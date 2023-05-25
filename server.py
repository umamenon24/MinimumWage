# flask --app data_server run
from flask import Flask
from flask import render_template
from flask import request
import json

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html')

app.run(debug=True)