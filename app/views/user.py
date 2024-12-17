from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.utils import *
from app.db.db import get_db, close_db


# Routes /user/...
user_bp = Blueprint('user', __name__, url_prefix='/user')

def get_appointments_for_user(user_id):

    db = get_db()
    cursor=db.cursor()

    cursor.execute('''
        SELECT date, heure, motif
        FROM "rendez-vous"
        WHERE id_personne = ? AND date >= date('now')
        ORDER BY date ASC, heure ASC
    ''', (user_id,))
    
    rdv = cursor.fetchall()
    
    close_db()
    
    return [
        {"date": appt[0], "heure": appt[1], "motif": appt[2]}
        for appt in rdv
    ]
    


@user_bp.route('/profile', methods=('GET', 'POST'))
@login_required 
def show_profile():
    user_id = session.get('id_personne')
    
    
    user_appointments = get_appointments_for_user(user_id)
    
    
    return render_template('user/profile.html', appointments = user_appointments)
