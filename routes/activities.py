# routes/activities.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from models import db, Activity, Grupo
from datetime import datetime
import pandas as pd
from io import BytesIO

activities_bp = Blueprint("activities", __name__)

@activities_bp.route("/dashboard")
@login_required
def dashboard():
    mes = request.args.get("mes", datetime.today().month, type=int)
    anio = request.args.get("anio", datetime.today().year, type=int)

    actividades = (
        Activity.query.filter(
            db.extract("month", Activity.fecha) == mes,
            db.extract("year", Activity.fecha) == anio,
            Activity.user_id == current_user.id,
        )
        .order_by(Activity.fecha.desc())
        .all()
    )
    return render_template("dashboard.html", actividades=actividades, mes=mes, anio=anio)

@activities_bp.route("/nueva_actividad", methods=["GET", "POST"])
@login_required
def nueva_actividad():
    if request.method == "POST":
        fecha = datetime.strptime(request.form["fecha"], "%Y-%m-%d").date()
        grupo_id = int(request.form["grupo_id"])
        descripcion = request.form["descripcion"]
        horas = request.form["horas"]

        nueva_act = Activity(
            fecha=fecha,
            grupo_id=grupo_id,
            descripcion=descripcion,
            horas=horas,
            user_id=current_user.id,
        )
        db.session.add(nueva_act)
        db.session.commit()
        flash("Actividad registrada exitosamente.")
        return redirect(url_for("activities.dashboard"))

    grupos = Grupo.query.filter_by(user_id=current_user.id).all()
    return render_template("nueva_actividad.html", grupos=grupos)

@activities_bp.route("/editar-actividad/<int:id>", methods=["GET", "POST"])
@login_required
def editar_actividad(id):
    actividad = Activity.query.get_or_404(id)

    if actividad.user_id != current_user.id:
        flash("No tienes permiso para editar esta actividad.")
        return redirect(url_for("activities.dashboard"))

    if request.method == "POST":
        actividad.fecha = datetime.strptime(request.form["fecha"], "%Y-%m-%d").date()
        actividad.grupo_id = int(request.form["grupo_id"])
        actividad.descripcion = request.form["descripcion"]
        actividad.horas = request.form["horas"]
        db.session.commit()
        flash("Actividad actualizada correctamente.")
        return redirect(url_for("activities.dashboard"))

    return render_template("editar_actividad.html", actividad=actividad)

@activities_bp.route("/eliminar-actividad/<int:id>", methods=["POST"])
@login_required
def eliminar_actividad(id):
    actividad = Activity.query.get_or_404(id)

    if actividad.user_id != current_user.id:
        flash("No tienes permiso para eliminar esta actividad.")
        return redirect(url_for("activities.dashboard"))

    db.session.delete(actividad)
    db.session.commit()
    flash("Actividad eliminada correctamente.")
    return redirect(url_for("activities.dashboard"))

@activities_bp.route("/exportar_actividades")
@login_required
def exportar_actividades():
    mes = int(request.args.get("mes", datetime.now().month))
    anio = int(request.args.get("anio", datetime.now().year))

    actividades = Activity.query.filter(
        db.extract("month", Activity.fecha) == mes,
        db.extract("year", Activity.fecha) == anio,
        Activity.user_id == current_user.id,
    ).all()

    df = pd.DataFrame(
        [
            {
                "Fecha": act.fecha.strftime("%Y-%m-%d"),
                "Grupo": act.grupo,
                "Descripción": act.descripcion,
                "Horas": act.horas,
            }
            for act in actividades
        ]
    )

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Actividades")

    output.seek(0)
    nombre_archivo = f"actividades_{anio}_{mes}.xlsx"
    return send_file(
        output,
        as_attachment=True,
        download_name=nombre_archivo,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )