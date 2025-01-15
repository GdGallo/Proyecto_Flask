from routes.api import api_bp
from routes.admin import admin_bp  
from langchain_module.controllers import langchain_bp
from users.routes import users_bp

def register_routes(app):
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(langchain_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api')