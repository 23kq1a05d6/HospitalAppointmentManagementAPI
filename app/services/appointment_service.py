from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreate


def create_appointment(
    db: Session,
    appointment_data: AppointmentCreate,
):
    overlapping_appointment = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == appointment_data.doctor_id,
            Appointment.appointment_start < appointment_data.appointment_end,
            Appointment.appointment_end > appointment_data.appointment_start,
        )
        .first()
    )

    if overlapping_appointment:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Doctor already has an overlapping appointment",
        )

    appointment = Appointment(**appointment_data.model_dump())

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment