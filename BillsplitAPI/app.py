# Flask utils
from flask import Flask, redirect, url_for, request, render_template, jsonify, abort
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///billsplit_database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.app_context().push()

@app.route('/', methods=['GET'])
def index():
    # Main page
    return "Hello World"
    
@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        user_username = request.form.get('username')
        user_mail = request.form.get('mail')

        if user_username and user_mail:
            new_user = User(user_username=user_username, user_mail=user_mail)
            try:
                db.session.add(new_user)
                db.session.commit()
            except Exception as e:
                return jsonify({"error": e}), 404
            return jsonify({"msg": "User Added Successfully!"}), 200
        else:
            return jsonify({"error": "Data not found"}), 404

    return jsonify({"error": "Not Found"}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    # Serve the app with gevent
    # http_server = WSGIServer(('0.0.0.0', 5000), app)
    # http_server.serve_forever()
