from flask import Flask, request, Response
import time
app = Flask(__name__)


data = None
flag = False


@app.route('/', methods=['POST'])
def print_data():
    print('\tPOST')
    filename = 'balances_post.txt'
    timestamp = int(time.time())
    with open(filename, 'a') as f:
        data ='{' + '"data":{}'.format(request.get_json()) + ', "timestamp":"{}"'.format(timestamp) + '}'
        print(str(data) + '\n\n')
        print(data, file = f)
    return 'something'


# @app.route("/stream", methods=['GET'])
# def stream():
#     print('\tGET')
#     print(str(data) + '\n\n')
#     def eventStream():
#
#         global flag
#         while True:
#             # Poll data from the database
#             # and see if there's a new message
#             print(flag)
#             if flag:
#                 flag = False
#                 yield data + '\n\n'
#             else:
#                 yield "data: None\n\n"
#
#     return app.response_class(
#         response=eventStream(),
#         status=200,
#         mimetype="text/event-stream",
#         headers={"Access-Control-Allow-Origin": "*"}
    # )
    # return Response(eventStream(), mimetype="text/event-stream")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
