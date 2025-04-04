import os
from flask import Flask
from app.utils import *
from flask_mail import Mail


mail = Mail()
# Importation des blueprints de l'application
# Chaque blueprint contient des routes pour l'application
from app.views.home import home_bp
from app.views.auth import auth_bp
from app.views.user import user_bp
from app.views.infos import informations_bp

from app.views.blogs import blogs_bp

# Fonction automatiquement appelée par le framework Flask lors de l'exécution de la commande python -m flask run permettant de lancer le projet
# La fonction retourne une instance de l'application créée
def create_app():

    # Crée l'application Flask
    app = Flask(__name__)
    app.config.from_pyfile(os.path.join(os.path.dirname(__file__),"config.py"))
    mail.init_app(app)
    

    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')

    

    from app.views.rendez_vous import rdv_bp
    # Enreigstrement des blueprints de l'application.
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(informations_bp)
    app.register_blueprint(rdv_bp)
    app.register_blueprint(blogs_bp)

    # On retourne l'instance de l'application Flask
    return app