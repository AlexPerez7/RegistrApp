from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Grupo

groups_bp = Blueprint('groups', __name__)

@groups_bp.route('/nuevo_grupo', methods=['GET', 'POST'])
@login_required
def nuevo_grupo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        if not nombre.strip():
            flash('El nombre del grupo no puede estar vacío.')
            return redirect(url_for('groups.nuevo_grupo'))

        if Grupo.query.filter_by(nombre=nombre, user_id=current_user.id).first():
            flash('Ya tienes un grupo con ese nombre.')
            return redirect(url_for('groups.nuevo_grupo'))

        nuevo = Grupo(nombre=nombre.strip(), user_id=current_user.id)
        db.session.add(nuevo)
        db.session.commit()
        flash('Grupo creado correctamente.')
        return redirect(url_for('nueva_actividad'))

    return render_template('nuevo_grupo.html')
