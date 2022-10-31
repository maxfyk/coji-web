import os

import requests
import requests as r
import validators
from flask import (Flask, Response, redirect, render_template, request)
from flask_cors import CORS

from static.constants import *

app = Flask(__name__)
CORS(app)
API_URL = os.environ.get('API_URL') or 'https://api.coji-code.com'
DATA_TYPES = ['text', 'url']  # , 'file'


# GET pages
# main page
@app.route('/', methods=['get'])
def index():
    """Main page"""
    return render_template('index.html')


# data preview page
@app.route('/data-preview/<id>', methods=['get'])
def data_preview(id):
    """Retrieve the encoded info"""
    resp = r.get(f'{API_URL}/coji-code/get/{id}')
    if resp.status_code == 200:
        code_info = resp.json().get('data', None)
        if not code_info:
            return render_template('error-page.html', ERROR='Code not found!')
        elif code_info['data-type'] == 'text':
            return render_template('data-preview-text.html', code_info=code_info)
        elif code_info['data-type'] == 'ar-model':
            return render_template('data-preview-ar.html', in_data=code_info['in-data'])
        elif code_info['data-type'] == 'url':
            return redirect(code_info['in-data'])
        return 'Not yet supported'
    elif resp.status_code == 422:
        return render_template('error-page.html', ERROR='Code not found!')

    return render_template('error-page.html', ERROR='Something went wrong!')


# create code page
@app.route('/create-code', methods=['get'])
def create_code():
    """Create a new code"""
    return render_template('create-code.html', data_types=DATA_TYPES)


# modify code page
@app.route('/modify-code', methods=['get'])
def modify_code():
    """Change code's information"""
    return render_template('modify-code.html', data_types=DATA_TYPES)


# map location page
@app.route('/location-decode/<location>', methods=['get'])
def location_decode(location):
    """Dummy map with codes"""
    resp = r.get(f'{API_URL}/coji-code/get-by-city/{location}')
    if resp.status_code == 200:
        codes = resp.json().get('data', None)
        return render_template('location-decode.html', CODES=enumerate(codes.items()), LOCATION=location)
    return render_template('index.html', ERROR='Something went wrong')


# keyboard decode page
@app.route('/keyboard-decode', methods=['get'])
def keyboard_decode():
    """Decode using keyboard"""
    return render_template('keyboard-decode.html')


# POST pages
@app.route('/keyboard-decode', methods=['post'])
def keyboard_decode_post():
    """Decode using keyboard (post)"""
    code_in = request.form.get('keyboard-decode-in', None)

    if code_in:
        in_data = DECODE_POST_JSON.copy()
        in_data['decode-type'] = 'keyboard'
        in_data['in-data'] = code_in
        in_data['user-data'] = None

        resp = r.post(f'{API_URL}/coji-code/decode', json=in_data)
        data = resp.json()
        if resp.status_code == 200 and not data.get('error'):
            return redirect('data-preview/' + data['code-id'], code=302)
        error = data.get('text') or 'Failed to decode your code, please try again later!'
    else:
        error = 'Please enter the code first!'
    return render_template('keyboard-decode.html', ERROR=error)


@app.route('/create-code-submit', methods=['post'])
def create_code_post():
    """Create a new code (post form)"""
    data_type = request.form.get('data-type', None)
    in_data = request.form.get(f'{data_type}-in', None)
    location = request.form.get('location-in', None)

    if data_type and in_data:
        if data_type == 'url' and validators.url(in_data) or data_type != 'url':
            data = CREATE_POST_JSON.copy()
            data['in-data'] = in_data
            data['data-type'] = data_type
            data['location'] = location
            resp = r.post(f'{API_URL}/coji-code/create', json=data)
            data = resp.json()
            if resp.status_code == 200 and not data.get('error'):
                return render_template('download-code.html', code_image=data['image'], char_code=data['code'])
            error = data.get('text') or 'Failed create a new code, try again later'
        else:
            error = 'You url is not valid!'
    else:
        error = 'Wrong values. Please try again!'
    return render_template('create-code.html', ERROR=error)


@app.route('/image-decode-request', methods=['post'])
def send_image_decode_request():
    """Forward request to api"""
    resp = requests.post(f'{API_URL}/coji-code/decode', json=request.get_json())
    return Response(resp.content, resp.status_code)


@app.route('/modify-code-submit', methods=['post'])
def modify_code_post():
    """Modify code's info( post form)"""
    data_type = request.form.get('data-type', None)
    in_data = request.form.get(f'{data_type}-in', None)
    code = request.form.get('code-in', None)

    if data_type and in_data and code:
        if data_type == 'url' and validators.url(in_data) or data_type != 'url':
            data = {
                'in-data': in_data,
                'data-type': data_type,
                'code-id': code,
                'style-info': {
                    'name': 'geom-original',
                },
                'user-id': None
            }
            resp = r.post(f'{API_URL}/coji-code/update', json=data)
            data = resp.json()
            if resp.status_code == 200 and not data.get('error'):
                return render_template('success-page.html')
            error = data.get('text') or 'Failed to modify your code, try again later'
        else:
            error = 'You url is not valid!'
    else:
        error = 'Wrong values. Please try again!'
    return render_template('modify-code.html', ERROR=error)


# static

@app.route('/scripts/main.js')
def scripts_main_js():
    return render_template('scripts/main.js', API_URL=API_URL)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
