from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db, close_db
import os




rdv_bp = Blueprint('rdv', __name__, url_prefix="/rdv")



@rdv_bp.route('/date', methods=('GET', 'POST')) 
def prendre_rendez_vous():
   


    if request.method == 'POST':

        
        
        heure = request.form.get['heure']
        date = request.form.get['date']
        motif = request.form.get['motif']
        

        
        db = get_db()

        
        if heure and date and motif:
            try:
                db.execute ("INSERT INTO rendez-vous (heure, date, motif) VALUES (?, ?, ?)",(heure, date, motif))
                # db.commit() permet de valider une modification de la base de données
                db.commit()
                # On ferme la connexion à la base de données pour éviter les fuites de mémoire
                close_db()
                return redirect(url_for("rdv.prendre_rendez_vous"))
            except db.IntegrityError:

                # La fonction flash dans Flask est utilisée pour stocker un message dans la session de l'utilisateur
                # dans le but de l'afficher ultérieurement, généralement sur la page suivante après une redirection
                error = "tous les champs doivent être rempli"
                flash(error)
    else:       
        return render_template('rdv/rendez-vous.html')


                
@rdv_bp.route('/horaire')
def horaire():
    
    selected_date = request.args.get('date')
   
    time_slots = {
        "08:00": "Occupied",
        "10:00": "Available",
        "12:00": "Available",
        "14:00": "Occupied",
        "16:00": "Available",
        "18:00": "Available"
    }
    return render_template('rdv/rendez-vous_horaire.html', date=selected_date, time_slots=time_slots)                
        
    
            


    
             