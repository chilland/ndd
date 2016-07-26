'''
    Generic Classifier Service
    ---------------------------

    To run:
        python generic-app.py -mv /path/to/model/directory

    Accepts urls to images in the format
        {
            "url" : "http://somewhere.com/image.jpg"
        }

    Returns
        {
            "label" : ... # Whether or not there is a match
            "score" : ... # Whether or not there is a match
            "model" : ... # Model that found the match
        }
'''

from __future__ import division
import sys
import json
import argparse
import logging
from flask import Flask, make_response, jsonify
from flask.ext.restful import Api, Resource, reqparse
from flask.ext.restful.representations.json import output_json
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from sklearn.externals import joblib
from generic_model import *

output_json.func_globals['settings'] = {
    'ensure_ascii' : False,
    'encoding' : 'utf8'
}

app = Flask(__name__)
api = Api(app)

logging.basicConfig(format='%(levelname)s %(asctime)s %(filename)s %(lineno)d: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def parse_arguments():
    parser = argparse.ArgumentParser(description=config['description'])
    parser._optionals.title = 'Options'
    parser.add_argument('-p', '--port', help='Specify port for API to listen on.',  type=str, required=False, default=5000)
    parser.add_argument('-mf', '--model-file', help='Specify model file.', type=str, required=True)
    return parser.parse_args()


class ClassifierAPI(Resource):
    def __init__(self, **kwargs):
        self.model = kwargs['model']
        self.config = kwargs['config']
        self.reqparse = reqparse.RequestParser()
        
        for arg in self.config['reqparse']:
            self.reqparse.add_argument(arg['field'], location=arg['location'])

        super(ClassifierAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        try:
            return model.predict_api(**args)
        except Exception as e:
            logger.info(e)
            return {}


class HealthCheck(Resource):
    def get(self):
        return make_response(jsonify({"status": "ok"}), 200)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
    

if __name__ == '__main__':
    config = json.load(open('/src/config.json'))
    
    logger.info('Starting service.')
    start_args = parse_arguments()
    port = start_args.port
    
    logger.info('Loading model.')
    model = apiModel(start_args.model_file)
    logger.info('Done loading model.')
    
    api.add_resource(ClassifierAPI, '/api/score', resource_class_kwargs={
        'model' : model,
        'config' : config
    })
    
    api.add_resource(HealthCheck, '/api/health')
    
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(port)
    IOLoop.instance().start()
