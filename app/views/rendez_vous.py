from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db, close_db
import os
from sqlite3 import connect
from datetime import datetime
from app.__init__ import mail
from flask_mail import Message


rdv_bp = Blueprint('rdv', __name__, url_prefix="/rdv")



@rdv_bp.route('/date', methods=('GET', 'POST')) 
def prendre_rendez_vous():
   
      
    return render_template('rdv/rendez-vous.html')


                
@rdv_bp.route('/horaire')
def horaire():
    
    selected_date = request.args.get('date')
   
    all_time_slots = [
        "08:00", "10:00", "12:00", "14:00", "16:00", "18:00"
    ]

    # Récupérer les horaires occupés depuis la base de données
    db = get_db()
    cur=db.cursor()
    cur.execute ('SELECT heure FROM "rendez-vous" WHERE date = ?', (selected_date, ))
    occupied_slots = [row[0] for row in cur.fetchall()]
    db.commit()
    close_db()

    # Créer un dictionnaire indiquant la disponibilité de chaque créneau
    time_slots = {
        slot: "Occupé" if slot in occupied_slots else "Disponible"
        for slot in all_time_slots
    }

    # Retourner le template avec les informations nécessaires
    return render_template('rdv/rendez-vous_horaire.html', date=selected_date, time_slots=time_slots)

              
        
    
            
@rdv_bp.route('/réserver', methods=['GET', 'POST'])
def reserver():
    selected_date = request.args.get('date')
    selected_time = request.args.get('time')
    
    if request.method == 'POST':
        user_id = session.get('id_personne')
        motif = request.form.get('motif')
        db = get_db()

        if selected_time and selected_date and motif and user_id:
            try:
               
                user = db.execute("SELECT email FROM personnes WHERE id_personne = ?", (user_id,)).fetchone()
                
                if user:
                    user_email = user[0]  

                    
                    db.execute("INSERT INTO 'rendez-vous' (heure, date, motif, id_personne) VALUES (?, ?, ?, ?)",
                               (selected_time, selected_date, motif, user_id))
                    db.commit()
                    close_db()

                    
                    msg = Message("Confirmation de votre rendez-vous",
                                  recipients=[user_email])
                    msg.body = f"""
                    Bonjour,

                    Votre rendez-vous a été confirmé avec les détails suivants :
                    - 📅 Date : {selected_date}
                    - ⏰ Heure : {selected_time}
                    - 📝 Motif : {motif}

                    Merci et à bientôt !
                    """
                    mail.send(msg)  
                    print(msg)

                    flash("Votre rendez-vous a été enregistré et un e-mail de confirmation a été envoyé.")

                else:
                    flash("Impossible de récupérer votre adresse e-mail.")

            except Exception as e:
                error = f"Une erreur s'est produite : {e}"
                flash(error)

            return redirect("/")
    
    return render_template('rdv/rendez-vous_motif.html', date=selected_date, time=selected_time)

    
@rdv_bp.route('/planing', methods=['GET', 'POST'])
def planing():
    selected_date = request.args.get('date')
    all_time_slots = [
        "08:00", "10:00", "12:00", "14:00", "16:00", "18:00"
    ]


    if not selected_date:
        selected_date = datetime.today().strftime('%Y-%m-%d')
    
    
    db = get_db()
    cur = db.cursor()

    
    cur.execute('''
        SELECT rv.heure, p.nom, rv.motif 
        FROM "rendez-vous" rv
        JOIN "personnes" p ON rv.id_personne = p.id_personne
        WHERE rv.date = ?
    ''', (selected_date,))
    
    reservations = cur.fetchall()
    occupied_slots = [row[0] for row in cur.fetchall()]
    db.commit()
    close_db()
    
    

    

    reservation_details = {row["heure"]: {"Nom": row["nom"], "Motif": row["motif"]} for row in reservations}


    time_slots = {
        slot: reservation_details[slot] if slot in reservation_details else "Disponible"
        for slot in all_time_slots
    }

    return render_template('rdv/rendez-vous_planing.html', date=selected_date, time_slots=time_slots)

    