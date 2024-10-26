from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)





rdv_bp = Blueprint('rdv', __name__,)



@rdv_bp.route('/rdv', methods=('GET', 'POST')) 
def prendre_rendez_vous():
   
    return render_template('rdv/rendez-vous.html')