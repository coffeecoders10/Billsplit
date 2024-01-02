# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    # Main page
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)

    # Serve the app with gevent
    # http_server = WSGIServer(('0.0.0.0', 5000), app)
    # http_server.serve_forever()
