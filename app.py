from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "smilecare_clave_secreta_prototipo"

# Almacenamiento temporal en memoria (sin base de datos en esta fase)
citas_registradas = [
    {
        "id": 1,
        "paciente": "Carlos Martínez",
        "telefono": "7845-1234",
        "fecha": "2026-11-18",
        "hora": "09:00",
        "tratamiento": "Limpieza Dental",
        "odontologo": "Dra. Sofía Méndez"
    }
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        paciente = request.form.get("paciente", "").strip()
        telefono = request.form.get("telefono", "").strip()
        fecha = request.form.get("fecha", "").strip()
        hora = request.form.get("hora", "").strip()
        tratamiento = request.form.get("tratamiento", "").strip()
        odontologo = request.form.get("odontologo", "").strip()

        # Validación de campos obligatorios
        if not all([paciente, telefono, fecha, hora, tratamiento, odontologo]):
            flash("Error: Todos los campos son obligatorios para agendar la cita.", "danger")
            return redirect(url_for("index"))

        # Validación de cruce de horarios para el mismo odontólogo
        for cita in citas_registradas:
            if cita["fecha"] == fecha and cita["hora"] == hora and cita["odontologo"] == odontologo:
                flash(f"Conflicto de horario: {odontologo} ya tiene una cita el {fecha} a las {hora}.", "warning")
                return redirect(url_for("index"))

        # Registro de la nueva cita en memoria
        nueva_cita = {
            "id": len(citas_registradas) + 1,
            "paciente": paciente,
            "telefono": telefono,
            "fecha": fecha,
            "hora": hora,
            "tratamiento": tratamiento,
            "odontologo": odontologo
        }
        citas_registradas.append(nueva_cita)
        flash(f"¡Cita registrada exitosamente para {paciente}!", "success")
        return redirect(url_for("index"))

    return render_template("index.html", citas=citas_registradas)

if __name__ == "__main__":
    app.run(debug=True)