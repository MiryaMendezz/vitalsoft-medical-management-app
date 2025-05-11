
Built by https://www.blackbox.ai

---

# VitalSoft

VitalSoft is a medical management application that allows healthcare providers to manage patients, doctors, appointments, medications, and medical histories. This application is built using Flask and SQLAlchemy, providing an intuitive interface for managing medical records and appointments.

## Project Overview

VitalSoft serves as a comprehensive healthcare management system that facilitates:
- Patient Registration
- Doctor Management
- Appointment Scheduling
- Medical Record Keeping

## Installation

To set up the VitalSoft project on your local environment, please follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://your-repository-url.git
   cd vitalsoft
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   Make sure you have Python 3.x and pip installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**:
   Run the `init_db.py` script to create the database and populate it with initial data:
   ```bash
   python init_db.py
   ```

5. **Start the application**:
   ```bash
   python app.py
   ```

6. **Access the application**:
   Open your browser and go to `http://127.0.0.1:5000`.

## Usage

1. **Login**: Use the credentials:
   - Email: `admin@vitalsoft.com`
   - Password: `admin123`

2. **Management Operations**:
   - Navigate through the application to manage:
     - Patients
     - Doctors
     - Appointments
     - Medications
     - Medical Histories

## Features

- User authentication with session management.
- Comprehensive management of patients, doctors, and medical histories.
- Appointment scheduling and tracking.
- Medication inventory management.
- Responsive web interface.

## Dependencies

The application requires the following Python packages, which can be found in the `requirements.txt` file:
- Flask
- Flask-SQLAlchemy
- Werkzeug

## Project Structure

```
vitalsoft/
├── app.py                # Main application file
├── config.py             # Configuration settings
├── init_db.py            # Script to initialize the database
├── models.py             # Database models
├── requirements.txt       # Package dependencies
└── templates/            # HTML templates for rendering views
```

### Database Models

- **Paciente**: Represents patients with attributes such as name, email, phone number, birth date, blood type, and medical records.
- **Doctor**: Represents doctors with details like name, email, specialty, and associated records.
- **Cita**: Represents appointments with references to patient and doctor.
- **HistoriaClinica**: Details the medical histories of patients.
- **Medicamento**: Stores information on medication available.
- **Usuario**: User model for the application with authentication capabilities.

## Contributing

Contributions to VitalSoft are welcome! Please feel free to submit a Pull Request or open an Issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.