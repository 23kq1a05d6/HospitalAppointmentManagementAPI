from datetime import datetime

from pydantic import BaseModel, ConfigDict, model_validator


class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_start: datetime
    appointment_end: datetime

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.appointment_start >= self.appointment_end:
            raise ValueError(
                "appointment_start must be before appointment_end"
            )
        return self


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentResponse(AppointmentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)