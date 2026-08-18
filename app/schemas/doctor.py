from pydantic import BaseModel, ConfigDict


class DoctorBase(BaseModel):
    name: str
    specialization: str


class DoctorCreate(DoctorBase):
    pass


class DoctorResponse(DoctorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)