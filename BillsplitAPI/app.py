# Flask utils
from flask import Flask, redirect, url_for, request, render_template, session, jsonify, abort
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from flask_oauthlib.client import OAuth
from dotenv import load_dotenv
import os
from models import *
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///billsplit_database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.app_context().push()

app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')

# Configure Google OAuth
oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key=os.getenv('GOOGLE_CLIENT_ID'),  # Replace with your Google OAuth client ID
    consumer_secret=os.getenv('GOOGLE_CLIENT_SECRET'),  # Replace with your Google OAuth client secret
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)



@app.route('/')
def index():
    # Main page
    if 'google_token' in session:
        user_info = google.get('userinfo')
        # Access user_info to get user details
        email = user_info.data['email']
        user_id = user_info.data['id']
        return f'Logged in as: {email}<br>Google User ID: {user_id}'
    return 'Not logged in'

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

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))

@app.route('/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')

    # Access user_info to get user details
    email = user_info.data['email']
    user_id = user_info.data['id']
    print(user_info)
    return 'Logged in as: ' + email + '<br>Google User ID: ' + user_id + '<br>user_info: '

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

@app.before_first_request
def create_database():
     db.create_all()


if __name__ == '__main__':
    app.run(debug=True)

    # Serve the app with gevent
    # http_server = WSGIServer(('0.0.0.0', 5000), app)
    # http_server.serve_forever()
