from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)



informations_bp = Blueprint('informations', __name__)


@informations_bp.route('/informations', methods=('GET', 'POST'))
def info():
   
    return render_template('infos/info.html')