import os
import requests as r
from flask import Flask, redirect, Response, url_for, render_template

app = Flask(__name__)
API_URL = os.environ.get('API_URL') or 'http://138.2.132.121'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data-preview/<id>')
def data_preview(id):
    resp = r.get(f'{API_URL}/coji-code/get/{id}')
    code_info = resp.json()['data']
    if not code_info:
        return render_template('error-page.html')
    elif code_info['data-type'] == 'text':
        return render_template('data-preview-text.html', code_info=code_info)
    elif code_info['data-type'] == 'url':
        return redirect(code_info['in-data'])
    return 'Not yet supported'


@app.route('/scripts/main.js')
def scripts_main_js():
    return render_template('scripts/main.js', API_URL=API_URL)


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
