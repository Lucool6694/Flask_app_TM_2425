from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.utils import *
from app.db.db import get_db, close_db


# Routes /user/...
user_bp = Blueprint('user', __name__, url_prefix='/user')

def get_appointments_for_user(user_id):

    db = get_db()
    cursor=db.cursor()

    db.execute('''
        SELECT date, heure, motif
        FROM "rendez-vous"
        WHERE id_personne = ? AND date >= date('now')
        ORDER BY date ASC, heure ASC
    ''', (user_id,))
    
    appointments = cursor.fetchall()
    print(appointments)
    
    
    return [
        {"date": appt[0], "heure": appt[1], "motif": appt[2]}
        for appt in appointments
    ]
    close_db()


# Route /user/profile accessible uniquement à un utilisateur connecté grâce au décorateur @login_required
@user_bp.route('/profile', methods=('GET', 'POST'))
@login_required 
def show_profile():
    user_id = session.get('id_personne')
    print(f"User ID: {user_id}")
    
    user_appointments = get_appointments_for_user(user_id)
    print(user_appointments)
    
    return render_template('user/profile.html', appointments = user_appointments)
