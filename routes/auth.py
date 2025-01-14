from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def auth_dashboard():
    return render_template ('auth.html', title ='Registro')