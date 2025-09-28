from flask import Flask
from .models import db
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object("instance.config.Config")

    db.init_app(app)
    Migrate(app, db)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app