from flask import Flask, request
import time
import json
import pymongo


app = Flask(__name__)


# If top > col.count() or top = 0 then col.count() documents will be returned


@app.route('/', methods=['GET'])
def hello_world():
    if 'pair' not in request.args:
        return app.response_class(
            response=json.dumps({'error': 'Mandatory parameter pair is absent'}),
            status=400,
            mimetype='application/json'
        )
    pair = request.args['pair']

    if 'top' not in request.args:
        top = 1
    else:
        top = int(request.args['top'])

    if top > 100:
        return app.response_class(
            response=json.dumps({'error': 'top must be not greater than 100'}),
            status=400,
            mimetype='application/json'
        )

    col_name = 'log_' + pair
    if col_name not in col_names:
        return app.response_class(
            response=json.dumps({'error': 'Wrong currency pair'}),
            status=400,
            mimetype='application/json'
        )

    col = db[col_name]
    try:
        return app.response_class(
            response=json.dumps(list(col.find(
                        projection={'_id': False},
                        limit=top,
                        sort=[("_id", pymongo.DESCENDING)])
            )),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        print(type(e))
        print()
        print(e)
        return app.response_class(
            response=json.dumps({'error': 'Some problems with database'}),
            status=500,
            mimetype='application/json'
        )


if __name__ == '__main__':
    client = pymongo.MongoClient("mongodb://admin:415096396771@23.100.25.146/admin")  # defaults to port 27017
    db = client['test_db']
    col_names = set(db.collection_names())

    col = db['log_btc_usd']
    col.drop()
    for i in range(30):
        d = {"timestamp": time.time(), "data": i+1}
        col.insert_one(d)
    app.run()
