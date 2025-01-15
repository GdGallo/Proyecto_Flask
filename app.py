from flask import Flask
from config import Config
from extensions import db, csrf, migrate
from routes import register_routes
from models import User

def create_app(): 
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    #csrf.init_app(app)
    migrate.init_app(app, db)
    register_routes(app)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
