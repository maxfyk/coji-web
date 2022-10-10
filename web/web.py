import os
import io
import base64
import validators
import requests as r
from flask import (
    Flask,
    redirect,
    request,
    render_template,
)

app = Flask(__name__)
API_URL = os.environ.get('API_URL') or 'https://coji-code.com'
DATA_TYPES = ['text', 'url']  # , 'file'


@app.route('/', methods=['get'])
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/data-preview/<id>', methods=['get'])
def data_preview(id):
    """Retrieve the encoded info"""
    resp = {'data': {'data-type': 'ar-model', 'in-data': {
        'glb-model-url': 'http://github.com/maxfyk/maxfyk.github.io/raw/master/assets/phoenix.glb',
        'position': '-2.8 2.35 -3.2', 'scale': '0.01 0.01 0.01'}, 'index': 37, 'style-info': {'name': 'geom-original'},
                     'time-created': '2022-10-07 09:56:06.391716', 'time-updated': '2022-10-07 09:56:06.391716'},
            'error': False}
    if resp:
        code_info = resp.get('data', None)
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


@app.route('/create-code', methods=['get'])
def create_code():
    """Create a new code"""
    return render_template('create-code.html', data_types=DATA_TYPES)


@app.route('/create-code-submit', methods=['post'])
def create_code_post():
    """Create a new code (post form)"""
    data_type = request.form.get('data-type', None)
    in_data = request.form.get(f'{data_type}-in', None)

    if data_type and in_data:
        if data_type == 'url' and validators.url(in_data) or data_type != 'url':
            in_data = {
                'in-data': in_data,
                'data-type': data_type,
                'style-info': {
                    'name': 'geom-original',
                },
                'user-id': None
            }
            resp = r.post(f'{API_URL}/coji-code/create', json=in_data)
            data = resp.json()
            if resp.status_code == 200 and not data.get('error'):
                return render_template('download-code.html', code_image=data['image'])
            error = data.get('text') or 'Failed create a new code, try again later'
        else:
            error = 'You url is not valid!'
    else:
        error = 'Wrong values. Please try again!'
    return render_template('error-page.html', ERROR=error)


# static

@app.route('/scripts/main.js')
def scripts_main_js():
    return render_template('scripts/main.js', API_URL=API_URL)


@app.route('/scripts/create-element.js')
def scripts_create_element_js():
    return render_template('scripts/create-element.js', API_URL=API_URL)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
