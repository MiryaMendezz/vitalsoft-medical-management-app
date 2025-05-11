from app import app, db
from models import Usuario, Paciente, Doctor, Cita, Medicamento, HistoriaClinica
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def init_db():
    with app.app_context():
        # Recreate all tables
        db.drop_all()
        db.create_all()

        # Create admin user
        admin = Usuario(
            email='admin@vitalsoft.com',
            password=generate_password_hash('admin123'),
            nombre='Administrador',
            rol='admin'
        )
        db.session.add(admin)

        # Create test doctors
        doctor1 = Doctor(
            nombre='Juan',
            apellido='Pérez',
            especialidad='Cardiología',
            email='juan.perez@vitalsoft.com',
            telefono='555-0101'
        )
        doctor2 = Doctor(
            nombre='María',
            apellido='García',
            especialidad='Pediatría',
            email='maria.garcia@vitalsoft.com',
            telefono='555-0102'
        )
        db.session.add_all([doctor1, doctor2])

        # Create test patients
        paciente1 = Paciente(
            nombre='Ana',
            apellido='López',
            email='ana.lopez@email.com',
            telefono='555-0201',
            fecha_nacimiento=datetime(1990, 5, 15),
            tipo_sangre='O+'
        )
        paciente2 = Paciente(
            nombre='Roberto',
            apellido='Martinez',
            email='roberto.martinez@email.com',
            telefono='555-0202',
            fecha_nacimiento=datetime(1985, 8, 22),
            tipo_sangre='A+'
        )
        db.session.add_all([paciente1, paciente2])

        # Create test medications
        med1 = Medicamento(
            nombre='Paracetamol',
            descripcion='Analgésico y antipirético',
            stock=100,
            stock_minimo=20
        )
        med2 = Medicamento(
            nombre='Ibuprofeno',
            descripcion='Antiinflamatorio no esteroideo',
            stock=80,
            stock_minimo=15
        )
        med3 = Medicamento(
            nombre='Amoxicilina',
            descripcion='Antibiótico de amplio espectro',
            stock=50,
            stock_minimo=10
        )
        db.session.add_all([med1, med2, med3])

        # Create test appointments
        cita1 = Cita(
            paciente_id=1,
            doctor_id=1,
            fecha_hora=datetime.now() + timedelta(days=1),
            motivo='Consulta rutinaria'
        )
        cita2 = Cita(
            paciente_id=2,
            doctor_id=2,
            fecha_hora=datetime.now() + timedelta(days=2),
            motivo='Control mensual'
        )
        db.session.add_all([cita1, cita2])

        # Create test medical histories
        historia1 = HistoriaClinica(
            paciente_id=1,
            doctor_id=1,
            fecha=datetime.now(),
            descripcion='Consulta por dolor en el pecho',
            diagnostico='Ansiedad',
            medicamentos='Paracetamol 500mg',
            tratamiento='Reposo y medicación'
        )
        historia2 = HistoriaClinica(
            paciente_id=2,
            doctor_id=2,
            fecha=datetime.now(),
            descripcion='Control pediátrico',
            diagnostico='Desarrollo normal',
            medicamentos='Ninguno',
            tratamiento='Continuar con controles mensuales'
        )
        db.session.add_all([historia1, historia2])

        # Commit all changes
        db.session.commit()

if __name__ == '__main__':
    init_db()
    print("Base de datos inicializada con datos de prueba.")
