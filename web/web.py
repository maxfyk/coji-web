import os
from flask import Flask, redirect, Response, url_for, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scripts/main.js')
def scripts_main_js():
    return render_template('scripts/main.js',
                           API_URL=os.environ['API_URL'])


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
