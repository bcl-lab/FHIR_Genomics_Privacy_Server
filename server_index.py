from flask_restful import Resource,Api,abort,reqparse
from flask import Flask
from resources import PrivacyList,Privacy
import subprocess
from argparse import ArgumentParser
from multiprocessing import cpu_count
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
api = Api(app)

api.add_resource(Privacy, '/Privacy')
api.add_resource(PrivacyList, '/Privacy/<id_>')

HOST = '127.0.0.1:5000'
PORT = 5000

if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('-d', '--debug', action='store_true')
    args = arg_parser.parse_args()
    if args.debug:
        #app.run(debug=True)
        #print 'here'
        app.debug= True
        app.config['SECRET_KEY'] = 'hadjhkwh'
        toolbar = DebugToolbarExtension()
        toolbar.init_app(app)
        app.run(port=PORT)
    else:
        #print 'there'
        num_workers = cpu_count() * 2 + 1
        cmd = 'gunicorn -w %d -b %s -D server:app --log-level error --log-file fhir.log'% (num_workers, HOST)
        subprocess.call(cmd, shell=True)
