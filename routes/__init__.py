from routes.api import api_bp
from routes.admin import admin_bp  
from routes.auth import auth_bp

def register_routes(app):
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')