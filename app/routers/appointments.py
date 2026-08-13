from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.services.appointment_service import check_overlap

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.get("", response_model=list[AppointmentResponse])
def get_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()


@router.post("", response_model=AppointmentResponse, status_code=201)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
):
    patient = db.query(Patient).filter(
        Patient.id == appointment.patient_id
    ).first()

    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    doctor = db.query(Doctor).filter(
        Doctor.id == appointment.doctor_id
    ).first()

    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if appointment.appointment_end <= appointment.appointment_start:
        raise HTTPException(
            status_code=400,
            detail="Appointment end must be after start",
        )

    check_overlap(
        db=db,
        doctor_id=appointment.doctor_id,
        new_start=appointment.appointment_start,
        new_end=appointment.appointment_end,
    )

    new_appointment = Appointment(**appointment.model_dump())
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found",
        )

    return appointment
