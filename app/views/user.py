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
   
def maj_user_info(user_id, nom, prenom, adresse, telephone):
    db = get_db()
    db.execute(
        'UPDATE personnes SET nom = ?, prenom = ?, adresse = ?, telephone = ? WHERE id_personne = ?',
        (nom, prenom, adresse, telephone, user_id)
    )
    db.commit()
    close_db()
 


@user_bp.route('/profile', methods=('GET', 'POST'))
@login_required 
def show_profile():
    user_id = session.get('id_personne')
    user_appointments = get_appointments_for_user(user_id)
    
    if request.method == 'POST':
        new_nom = request.form.get('nom')
        new_prenom = request.form.get('prenom')
        new_adresse = request.form.get('adresse')
        new_telephone = request.form.get('telephone')
        
        if new_nom and new_prenom and new_adresse and new_telephone:
            maj_user_info(user_id, new_nom, new_prenom, new_adresse, new_telephone)  
            flash("Profil mis à jour avec succès.", "succes")
            return redirect(url_for('user.show_profile'))

        else:
            flash("Veuillez remplir tous les champs.", "Attention")
    
    
    
    
    return render_template('user/profile.html', appointments = user_appointments)
