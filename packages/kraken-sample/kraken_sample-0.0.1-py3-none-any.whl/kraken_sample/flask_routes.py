
import datetime
import html
from flask import Flask
from flask import request
from flask import Response
from flask import redirect
from flask import url_for
from flask import jsonify
from flask import flash
from flask import render_template

from kraken_sample.records import records
from kraken_sample.helpers import json

UPLOAD_FOLDER = '/path/to/the/uploads'

# Initialize flask app
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')
app.secret_key = b'_5#mn"F4Q8znxec]/'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




@app.route('/')
def main_get():

    record_types = records.record_types()
    
    
    return Response(render_template('main.html', record_types=record_types))

@app.route('/<record_type>')
def record_type_get(record_type):

    id = request.args.get('id')
    
    record_sample = records.get(record_type)

    json_record = json.dumps(record_sample)
    content = json_record.replace('\n', '<br>')
    content = content.replace(' ', '&nbsp&nbsp')

    html_record = html.escape(json_record)

    return Response(render_template('sample_record.html', record=json_record, content=content))

def run_api():
    app.run(host='0.0.0.0', debug=False)

