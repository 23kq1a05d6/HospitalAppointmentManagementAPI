# Hospital Appointment Management API

FastAPI hospital appointment management project based on the provided assignment.

## Models
- Patient
- Doctor
- Appointment

## API operations
- GET /patients
- POST /patients
- GET /patients/{id}
- GET /doctors
- POST /doctors
- GET /doctors/{id}
- GET /appointments
- POST /appointments
- GET /appointments/{id}

## Business rule
A doctor cannot have overlapping appointments.

## Technologies
FastAPI, Pydantic, SQLAlchemy, Alembic, Pytest, Ruff, Bandit.
