from flask import Flask, request, Response
from logger_mongo import run_logger
from multiprocessing import Process
import time
import json
import logging
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
    N.B. All responses have
    (*) mimetype "applicaiton/json"
    (*) header "Access-Control-Allow-Origin" with value "*"
    """

    if "pair" not in request.args:
        return app.response_class(
            response=json.dumps({"error": "Mandatory parameter 'pair' is absent"}),
            status=400,
            mimetype="application/json",
            headers={"Access-Control-Allow-Origin": "*"}
        )
    col_name = prefix + request.args["pair"]
    if col_name not in col_names:
        return app.response_class(
            response=json.dumps({"error": 'Not supported currency pair'}),
            status=400,
            mimetype="application/json",
            headers={"Access-Control-Allow-Origin": "*"}
        )

    if "top" not in request.args:
        top = 1
    else:
        try:
            top = int(request.args["top"])
        except ValueError:
            return app.response_class(
                response=json.dumps({"error": "Parameter 'top' must be non-negative integer"}),
                status=400,
                mimetype="application/json",
                headers={"Access-Control-Allow-Origin": "*"}
            )
    if top < top_min or top > top_max:
        return app.response_class(
            response=json.dumps({"error": "Parameter 'top' must satisfy inequality 0 < 'top' <= 100"}),
            status=400,
            mimetype="application/json",
            headers={"Access-Control-Allow-Origin": "*"}
        )

    col = db[col_name]
    try:
        return app.response_class(
            response=json.dumps(list(col.find(
                        projection={"_id": False},
                        limit=top,
                        sort=[("_id", pymongo.DESCENDING)])
            )),
            status=200,
            mimetype="application/json",
            headers={"Access-Control-Allow-Origin": "*"}
        )
    except Exception as e:
        print(type(e))
        print()
        print(e)
        return app.response_class(
            response=json.dumps({"error": "Some problems with database occurred"}),
            status=500,
            mimetype="application/json",
            headers={"Access-Control-Allow-Origin": "*"}
        )


@app.route('/get_pairs', methods=['GET'])
def get_pairs():
    return app.response_class(
        response=json.dumps(trading_symbols),
        status=200,
        mimetype="application/json",
        headers={"Access-Control-Allow-Origin": "*"}
    )


@app.route('/get_tech', methods=['GET'])
def get_tech_data():
    return get_data('tech_')


@app.route('/', methods=['GET'])
def get_log_data():
    return get_data('log_')


if __name__ == '__main__':
    # Initialization
    mongo_config = json.load(open('mongo_credentials.json'))
    mongo_path = mongo_config['auth_string']
    client = pymongo.MongoClient(mongo_path)  # defaults to port 27017
    db_name = mongo_config['database']
    db = client[db_name]
    col_names = set(db.collection_names())

    # Logging to MongoDB
    trading_symbols = sorted(['bch_btc', 'bch_usd', 'dash_btc', 'eth_btc', 'btc_usd',
                              'xrp_btc', 'dash_usd', 'eth_usd', 'xrp_usd'])
    limit = 50
    config_file = mongo_config['orders_config']
    for symbol in trading_symbols:
        p = Process(target=run_logger, args=(symbol, limit, config_file, mongo_path, db_name))
        p.start()
        time.sleep(0.3)

    # Flask logging
    logger = logging.getLogger('werkzeug')
    handler = logging.FileHandler('access.log')
    logger.addHandler(handler)
    app.logger.addHandler(handler)

    # Starting server
    app.run(host='0.0.0.0')
