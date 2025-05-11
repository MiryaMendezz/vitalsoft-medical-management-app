from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config
from models import db, Paciente, Doctor, Cita, HistoriaClinica, Medicamento, Usuario
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()
    # Create default admin user if not exists
    if not Usuario.query.filter_by(email='admin@vitalsoft.com').first():
        admin = Usuario(
            email='admin@vitalsoft.com',
            password=generate_password_hash('admin123'),
            nombre='Administrador',
            rol='admin'
        )
        db.session.add(admin)
        db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Usuario.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_email'] = user.email
            return redirect(url_for('index'))
        flash('Credenciales inválidas', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    total_pacientes = Paciente.query.count()
    total_doctores = Doctor.query.count()
    total_citas = Cita.query.count()
    total_medicamentos = Medicamento.query.count()
    citas = Cita.query.order_by(Cita.fecha_hora).limit(5).all()
    return render_template('index.html', 
                         total_pacientes=total_pacientes,
                         total_doctores=total_doctores,
                         total_citas=total_citas,
                         total_medicamentos=total_medicamentos,
                         citas=citas)

@app.route('/patients')
def patients():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    pacientes = Paciente.query.all()
    return render_template('patients.html', pacientes=pacientes)

@app.route('/patients/edit/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    paciente = Paciente.query.get_or_404(patient_id)
    if request.method == 'POST':
        paciente.nombre = request.form.get('nombre')
        paciente.apellido = request.form.get('apellido')
        paciente.email = request.form.get('email')
        paciente.telefono = request.form.get('telefono')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        paciente.fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d') if fecha_nacimiento else None
        paciente.tipo_sangre = request.form.get('tipo_sangre')
        db.session.commit()
        flash('Paciente actualizado exitosamente.', 'success')
        return redirect(url_for('patients'))
    return render_template('edit_patient.html', paciente=paciente)

@app.route('/patients/delete/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    paciente = Paciente.query.get_or_404(patient_id)
    db.session.delete(paciente)
    db.session.commit()
    flash('Paciente eliminado exitosamente.', 'success')
    return redirect(url_for('patients'))

@app.route('/doctors')
def doctors():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    doctores = Doctor.query.all()
    return render_template('doctors.html', doctores=doctores)

@app.route('/doctors/edit/<int:doctor_id>', methods=['GET', 'POST'])
def edit_doctor(doctor_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    doctor = Doctor.query.get_or_404(doctor_id)
    if request.method == 'POST':
        doctor.nombre = request.form.get('nombre')
        doctor.apellido = request.form.get('apellido')
        doctor.email = request.form.get('email')
        doctor.telefono = request.form.get('telefono')
        doctor.especialidad = request.form.get('especialidad')
        db.session.commit()
        flash('Doctor actualizado exitosamente.', 'success')
        return redirect(url_for('doctors'))
    return render_template('edit_doctor.html', doctor=doctor)

@app.route('/doctors/delete/<int:doctor_id>', methods=['POST'])
def delete_doctor(doctor_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    doctor = Doctor.query.get_or_404(doctor_id)
    db.session.delete(doctor)
    db.session.commit()
    flash('Doctor eliminado exitosamente.', 'success')
    return redirect(url_for('doctors'))

@app.route('/doctors/add', methods=['GET', 'POST'])
def add_doctor():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        especialidad = request.form.get('especialidad')

        if not nombre or not apellido or not email:
            flash('Por favor, complete los campos obligatorios.', 'error')
            return redirect(url_for('add_doctor'))

        doctor = Doctor(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            especialidad=especialidad
        )
        db.session.add(doctor)
        db.session.commit()
        flash('Doctor registrado exitosamente.', 'success')
        return redirect(url_for('doctors'))
    return render_template('add_doctor.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        tipo_sangre = request.form.get('tipo_sangre')

        if not nombre or not apellido or not email:
            flash('Por favor, complete los campos obligatorios.', 'error')
            return redirect(url_for('register'))

        paciente = Paciente(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            fecha_nacimiento=datetime.strptime(fecha_nacimiento, '%Y-%m-%d') if fecha_nacimiento else None,
            tipo_sangre=tipo_sangre
        )
        db.session.add(paciente)
        db.session.commit()
        flash('Paciente registrado exitosamente.', 'success')
        return redirect(url_for('patients'))
    return render_template('register.html')

@app.route('/medications')
def medications():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    medicamentos = Medicamento.query.all()
    return render_template('medications.html', medicamentos=medicamentos)

@app.route('/medications/add', methods=['GET', 'POST'])
def add_medication():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        stock = request.form.get('stock')
        stock_minimo = request.form.get('stock_minimo')

        if not nombre or not descripcion or not stock or not stock_minimo:
            flash('Por favor, complete todos los campos obligatorios.', 'error')
            return redirect(url_for('add_medication'))

        medicamento = Medicamento(
            nombre=nombre,
            descripcion=descripcion,
            stock=int(stock),
            stock_minimo=int(stock_minimo)
        )
        db.session.add(medicamento)
        db.session.commit()
        flash('Medicamento agregado exitosamente.', 'success')
        return redirect(url_for('medications'))
    return render_template('add_medication.html')

@app.route('/medications/edit/<int:medication_id>', methods=['GET', 'POST'])
def edit_medication(medication_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    medicamento = Medicamento.query.get_or_404(medication_id)
    if request.method == 'POST':
        medicamento.nombre = request.form.get('nombre')
        medicamento.descripcion = request.form.get('descripcion')
        medicamento.stock = int(request.form.get('stock'))
        medicamento.stock_minimo = int(request.form.get('stock_minimo'))
        db.session.commit()
        flash('Medicamento actualizado exitosamente.', 'success')
        return redirect(url_for('medications'))
    return render_template('edit_medication.html', medicamento=medicamento)

@app.route('/medications/delete/<int:medication_id>', methods=['POST'])
def delete_medication(medication_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    medicamento = Medicamento.query.get_or_404(medication_id)
    db.session.delete(medicamento)
    db.session.commit()
    flash('Medicamento eliminado exitosamente.', 'success')
    return redirect(url_for('medications'))

@app.route('/histories')
def histories():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    historias = HistoriaClinica.query.all()
    return render_template('histories.html', historias=historias)

@app.route('/histories/add', methods=['GET', 'POST'])
def add_history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        paciente_id = request.form.get('paciente_id')
        doctor_id = request.form.get('doctor_id')
        descripcion = request.form.get('descripcion')
        fecha = request.form.get('fecha')
        medicamentos = request.form.get('medicamentos')
        diagnostico = request.form.get('diagnostico')
        tratamiento = request.form.get('tratamiento')

        if not paciente_id or not doctor_id or not descripcion:
            flash('Por favor, complete los campos obligatorios.', 'error')
            return redirect(url_for('add_history'))

        historia = HistoriaClinica(
            paciente_id=int(paciente_id),
            doctor_id=int(doctor_id),
            descripcion=descripcion,
            fecha=datetime.strptime(fecha, '%Y-%m-%d') if fecha else datetime.utcnow(),
            medicamentos=medicamentos,
            diagnostico=diagnostico,
            tratamiento=tratamiento
        )
        db.session.add(historia)
        db.session.commit()
        flash('Historia clínica agregada exitosamente.', 'success')
        return redirect(url_for('histories'))

    pacientes = Paciente.query.all()
    doctores = Doctor.query.all()
    medicamentos = Medicamento.query.all()
    return render_template('add_history.html', pacientes=pacientes, doctores=doctores, medicamentos=medicamentos)

@app.route('/histories/edit/<int:history_id>', methods=['GET', 'POST'])
def edit_history(history_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    historia = HistoriaClinica.query.get_or_404(history_id)
    if request.method == 'POST':
        historia.paciente_id = int(request.form.get('paciente_id'))
        historia.doctor_id = int(request.form.get('doctor_id'))
        historia.descripcion = request.form.get('descripcion')
        fecha = request.form.get('fecha')
        historia.fecha = datetime.strptime(fecha, '%Y-%m-%d') if fecha else historia.fecha
        historia.medicamentos = request.form.get('medicamentos')
        historia.diagnostico = request.form.get('diagnostico')
        historia.tratamiento = request.form.get('tratamiento')
        db.session.commit()
        flash('Historia clínica actualizada exitosamente.', 'success')
        return redirect(url_for('histories'))

    pacientes = Paciente.query.all()
    doctores = Doctor.query.all()
    medicamentos = Medicamento.query.all()
    return render_template('edit_history.html', historia=historia, pacientes=pacientes, doctores=doctores, medicamentos=medicamentos)

@app.route('/histories/delete/<int:history_id>', methods=['POST'])
def delete_history(history_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    historia = HistoriaClinica.query.get_or_404(history_id)
    db.session.delete(historia)
    db.session.commit()
    flash('Historia clínica eliminada exitosamente.', 'success')
    return redirect(url_for('histories'))

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    doctores = Doctor.query.all()
    pacientes = Paciente.query.all()
    if request.method == 'POST':
        paciente_id = request.form.get('paciente_id')
        doctor_id = request.form.get('doctor_id')
        fecha_hora = request.form.get('fecha_hora')
        motivo = request.form.get('motivo')

        if not paciente_id or not doctor_id or not fecha_hora:
            flash('Por favor, complete todos los campos obligatorios.', 'error')
            return redirect(url_for('appointments'))

        cita = Cita(
            paciente_id=int(paciente_id),
            doctor_id=int(doctor_id),
            fecha_hora=datetime.strptime(fecha_hora, '%Y-%m-%dT%H:%M'),
            motivo=motivo
        )
        db.session.add(cita)
        db.session.commit()
        flash('Cita agendada exitosamente.', 'success')
        return redirect(url_for('index'))
    return render_template('appointments.html', doctores=doctores, pacientes=pacientes)

if __name__ == '__main__':
    app.run(debug=True)
