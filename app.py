# app.py

from flask import Flask, render_template
from flask_login import LoginManager
from models import db, User
from routes.auth import auth
from routes.groups import groups_bp
from routes.activities import activities_bp

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "123456789"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///registro.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints
    app.register_blueprint(auth)
    app.register_blueprint(groups_bp)
    app.register_blueprint(activities_bp)

    @app.route("/")
    def index():
        return render_template("base.html")

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)