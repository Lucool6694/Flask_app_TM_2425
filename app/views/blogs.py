from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)



blogs_bp = Blueprint('blogs', __name__)


@blogs_bp.route('/blogs', methods=('GET', 'POST'))
def blogs():
   
    return render_template('blog/blog.html')