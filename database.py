from flask_sqlalchemy import SQLAlchemy
import Config

conf = Config.Config()

db = SQLAlchemy()

def create_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = conf.SQLALCHEMY_DATABASE_URI
    db.init_app(app)
    return db
