from flask import Flask
from flask_login import LoginManager
from db import db
from pymongo import MongoClient
from config import SECRET_KEY
from flask import Flask, render_template
from bson import ObjectId
from controllers.feature.admin_routes import admin_bp
from controllers.feature.user_routes import user_bp
from controllers.feature.upload_routes import upload_bp
from controllers.feature.review_routes import review_bp
from controllers.feature.payment_routes import payment_bp


app = Flask(__name__)
app.secret_key = "4NdrO0mAq3zkMPwrv7q9A0nqK2dJFOSs"


# MongoDB Setup
client = MongoClient("mongodb://localhost:27017")
db = client['conference_db']

@app.route('/')
def home():
    return render_template('home.html')

# Flask-Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'

from models.user import User

@login_manager.user_loader
def load_user(user_id):
    user_data = db.users.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None

# Register Blueprints
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(upload_bp, url_prefix='/upload')
app.register_blueprint(review_bp, url_prefix='/review')
app.register_blueprint(payment_bp, url_prefix='/payment')

if __name__ == "__main__":
    app.run(debug=True)
