from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from constants import DB_PATH

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"

    db.init_app(app)

    migrate = Migrate(app, db)

    from routes import register_routes
    register_routes(app, db)
    
    return app