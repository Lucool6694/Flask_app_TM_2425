import os
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app)
from app.db.db import get_db, close_db
from werkzeug.utils import secure_filename


blogs_bp = Blueprint('blogs', __name__)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@blogs_bp.route('/blogs', methods=('GET', 'POST'))
def blogs():
   
    if request.method == 'POST':

        
        
        titre = request.form['title']
        texte = request.form ['content']
        image= request.files['image']
        

        
        db = get_db()

       
        if titre and texte and image :
            try:


                upload_folder = current_app.config['UPLOAD_FOLDER']
                    
                    
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)

                if allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image_path = os.path.join(upload_folder, filename)
                    image.save(image_path)

                db.execute ("INSERT INTO articles (titre, texte, image) VALUES (?, ?, ?)",(titre, texte, filename))
                
                db.commit()
                
                close_db()
                return render_template('blog/blog.html')
            except db.IntegrityError:


                error = "tous les champs doivent être rempli"
                flash(error)


    else:
        return render_template('blog/blog.html')
