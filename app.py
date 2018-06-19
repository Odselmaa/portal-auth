import json

import bson
from bson import ObjectId
from flask import Flask
from flask_mongoengine import MongoEngine
from werkzeug.exceptions import BadRequest, Unauthorized, NotFound
from flask import jsonify, request
import jwt
from controller import *
import requests

app = Flask(__name__)
app.config['MONGODB_DB'] = 'Portal'
app.config[
    'MONGODB_HOST'] = 'mongodb://admin:s4WbwyymZ2R1vLVC@cluster0-shard-00-00-dkvkd.mongodb.net:27017,cluster0-shard-00-01-dkvkd.mongodb.net:27017,cluster0-shard-00-02-dkvkd.mongodb.net:27017/Portal?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true'
app.config['MONGODB_USERNAME'] = 'admin'
app.config['MONGODB_PASSWORD'] = 's4WbwyymZ2R1vLVC'
db = MongoEngine()
db.init_app(app)


@app.route("/api/token", methods=["GET","POST"])
def add_token():
    if request.method == 'POST':
        payload = request.json
        print(payload)
        at = add_access_token(payload)

        return jsonify({'statusCode': 200, 'response': {'id':str(at.id)}}), 200
    else:
        tokens = get_access_tokens()
        return jsonify({'statusCode': 200, 'response': tokens})


@app.route("/api/check_authorization/<string:token>", methods=["GET"])
def check_authorization(token):
    at = get_access_token(token)
    if at is not None:
        expired_when = at.expired_when
        if expired_when > datetime.datetime.now():
            return jsonify({"statusCode": 200, "response": "OK"}), 200
        else:
            raise Unauthorized
    else:
        raise NotFound


@app.errorhandler(BadRequest)
def global_handler_bad_request(e):
    print(e)
    return jsonify({'statusCode': 401, 'response': str(e)}), 401


@app.errorhandler(bson.errors.InvalidId)
@app.errorhandler(NotFound)
def global_handler_not_found(e):
    return jsonify({'statusCode': 404, 'response': 'Not found'}), 404



def is_valid_id(_id):
    return len(_id)==24 and _id is not None

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)
