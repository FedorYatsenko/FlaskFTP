from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from auth import login_required
from db import get_db

bp = Blueprint('files', __name__)


@bp.route('/')
def index():
    db = get_db()
    files = db.execute(
        'SELECT uf.id, file_name, loaded, user_id, u.username user_name'
        ' FROM user_file uf JOIN user u ON uf.user_id = u.id'
        ' ORDER BY loaded DESC'
    ).fetchall()
    return render_template('files/index.html', files=files)


@bp.route('/upload', methods=('GET', 'POST'))
@login_required
def upload():
    if request.method == 'POST':
        file_name = request.form['file_name']
        error = None

        if not file_name:
            error = 'File name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO user_file (file_name, user_id)'
                ' VALUES (?, ?)',
                (file_name, g.user['id'])
            )
            db.commit()
            return redirect(url_for('files.index'))

    return render_template('files/upload.html')


@bp.route('/my_files')
@login_required
def my_files():
    db = get_db()
    files = db.execute(
        'SELECT uf.id, file_name, loaded'
        ' FROM user_file uf JOIN user u ON uf.user_id = u.id'
        ' WHERE uf.user_id == (?)'
        ' ORDER BY loaded DESC',
        (g.user['id'], )
    ).fetchall()
    return render_template('files/my_files.html', files=files)

