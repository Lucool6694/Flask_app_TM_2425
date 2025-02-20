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
    db = get_db()
    query = "SELECT id_articles, titre, texte, image FROM articles ORDER BY id_articles DESC LIMIT 2"
    cursor = db.execute(query)
    posts = cursor.fetchall()

    if request.method == 'POST':
        if "edit_post_id" in request.form:  #Détecte si l'utilisateur veut éditer un blog existant
            return edit_post(request.form, request.files)
        else:  #Sinon, l'utilisateur veut créer un nouveau blog
            titre = request.form['title']
            texte = request.form['content']
            image = request.files['image']

            if titre and texte and image:
                try:
                    upload_folder = current_app.config['UPLOAD_FOLDER']

                    if not os.path.exists(upload_folder):
                        os.makedirs(upload_folder)

                    if allowed_file(image.filename):
                        filename = secure_filename(image.filename)
                        image_path = os.path.join(upload_folder, filename)
                        image.save(image_path)

                        db.execute("INSERT INTO articles (titre, texte, image) VALUES (?, ?, ?)", (titre, texte, filename))
                        db.commit()

                    close_db()
                    return redirect(url_for('blogs.blogs')) 
                except Exception as e:
                    flash("Erreur: " + str(e))

    close_db()
    return render_template('blog/blog.html', posts=posts)

#Permet d'editer un blog existant
def edit_post(form, files):
    post_id = form.get('edit_post_id')
    titre = form.get('edit_title')
    texte = form.get('edit_content')
    image = files.get('edit_image')

    if post_id and titre and texte:
        try:
            db = get_db()
            if image and allowed_file(image.filename):  # If a new image is uploaded
                filename = secure_filename(image.filename)
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                db.execute("UPDATE articles SET titre = ?, texte = ?, image = ? WHERE id_articles = ?", 
                           (titre, texte, filename, post_id))
            else:
                db.execute("UPDATE articles SET titre = ?, texte = ? WHERE id_articles = ?", 
                           (titre, texte, post_id))

            db.commit()
            close_db()

            return jsonify({"success": True, "titre": titre, "texte": texte, 
                            "image_url": url_for('static', filename=f"uploads/{filename}") if image else None})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})

    return jsonify({"success": False, "error": "Missing data"})
