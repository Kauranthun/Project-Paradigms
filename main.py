from flask import Flask
from config import Config
from app.models.models import db, User, bcrypt
from app.routes.photos import photo_bp
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'photos.login'

app.register_blueprint(photo_bp)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User,int(user_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,host="0.0.0.0", port=5000)