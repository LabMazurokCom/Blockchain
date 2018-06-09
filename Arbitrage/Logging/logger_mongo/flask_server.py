"""
All responses have
    mimetype="application/json",
    headers={"Access-Control-Allow-Origin": "*"}
"""


from flask import Flask, request, Response
from logger_mongo import run_logger
from multiprocessing import Process
import time
import json
import logging
import pprint
import pymongo


app = Flask(__name__)


# If top > col.count() or top = 0 then col.count() documents will be returned


def get_data(prefix, top_min=1, top_max=100):
    """
    Returns request.args["top"] last entries from prefix+request.args["pair"]
    :param prefix: prefix of collection to be used: log_ or tech_
    :param top_min: minimum allowed number of last orders to be requested
    :param top_max: maximum allowed number of last orders to be requested
    :return: Flask response_class with appropriate status and error message if required
    """

    # Processing 'pair' parameter
    if "pair" not in request.args:
        return {"error": "Mandatory parameter 'pair' is absent"}, 400
    col_name = prefix + request.args["pair"]
    if col_name not in col_names:
        return {"error": 'Not supported currency pair'}, 400

    # Processing 'top' parameter (if present)
    if "top" not in request.args:
        top = 1
    else:
        try:
            top = int(request.args["top"])
        except ValueError:
            return {"error": "Parameter 'top' must be non-negative integer"}, 400
    if top < top_min or top > top_max:
        return {"error": "Parameter 'top' must satisfy inequality 0 < 'top' <= 100"}, 400

    # Fetching 'top' last entries for 'pair' from database
    col = db[col_name]
    try:
        db_response = list(col.find(
                        projection={"_id": False},
                        limit=top,
                        sort=[("_id", pymongo.DESCENDING)])
            )
        return db_response, 200
    except Exception as e:
        print(type(e))
        print(e)
        return {"error": "Some problems with database occurred"}, 500


def generate_response(data, status):
    # Processing 'pretty' parameter
    if "pretty" not in request.args:
        pretty = False
    else:
        if request.args["pretty"] == "1":
            pretty = True
        else:
            pretty = False

    if pretty:
        return app.response_class(
            response=pprint.pformat(data),
            status=status,
            mimetype="text/plain",
            headers={"Access-Control-Allow-Origin": "*"}
        )
    else:
        return app.response_class(
            response=json.dumps(data),
            status=status,
            mimetype="application/json",
            headers={"Access-Control-Allow-Origin": "*"}
        )


@app.route('/get_pairs', methods=['GET'])
def get_pairs():
    data = pairs
    status = 200
    return generate_response(data, status)


@app.route('/get_tech', methods=['GET'])
def get_tech_data():
    data, status = get_data('tech_')
    return generate_response(data, status)


@app.route('/', methods=['GET'])
def get_log_data():
    data, status = get_data('log_')
    return generate_response(data, status)


if __name__ == '__main__':
    # Initialization
    mongo_config = json.load(open('mongo_config.json'))
    mongo_path = mongo_config['auth_string']
    db_name = mongo_config['database']
    config_file = mongo_config['orders_config']
    limit = mongo_config['limit']
    pairs = mongo_config['pairs']

    # Logging to MongoDB
    # for pair in pairs:
    #     p = Process(target=run_logger, args=(pair, limit, config_file, mongo_path, db_name))
    #     p.start()
    #     time.sleep(0.3)
    # time.sleep(120)

    # Connecting to database for server requests
    client = pymongo.MongoClient(mongo_path)  # defaults to port 27017
    db = client[db_name]
    col_names = set(db.collection_names())

    # Flask logging
    logger = logging.getLogger('werkzeug')
    handler = logging.FileHandler('access.log')
    logger.addHandler(handler)
    app.logger.addHandler(handler)

    # Starting server
    app.run(host='0.0.0.0')
