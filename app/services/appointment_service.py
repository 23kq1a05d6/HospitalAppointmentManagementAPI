from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.appointment import Appointment


def check_overlap(
    db: Session,
    doctor_id: int,
    new_start,
    new_end,
):
    existing = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.appointment_start < new_end,
        Appointment.appointment_end > new_start,
    ).first()

    if existing is not None:
        raise HTTPException(
            status_code=409,
            detail="Doctor already has an appointment at this time",
        )
