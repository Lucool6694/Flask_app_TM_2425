from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.db.db import get_db, close_db
# Routes /...
home_bp = Blueprint('home', __name__)



# Route /
@home_bp.route('/', methods=('GET', 'POST'))
def landing_page():
    # Affichage de la page principale de l'application
    
    query = "SELECT titre, texte, image FROM articles ORDER BY id_articles DESC LIMIT 2"
    db = get_db()
    cursor = db.execute(query)
    posts = cursor.fetchall()
    close_db()
    return render_template('home/index.html', posts=posts)

# Gestionnaire d'erreur 404 pour toutes les routes inconnues
@home_bp.route('/<path:text>', methods=['GET', 'POST'])
def not_found_error(text):
    return render_template('home/404.html'), 404
