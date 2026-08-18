from pydantic import BaseModel, ConfigDict, EmailStr


class PatientBase(BaseModel):
    name: str
    email: EmailStr
    phone: str


class PatientCreate(PatientBase):
    pass


class PatientResponse(PatientBase):
    id: int

    model_config = ConfigDict(from_attributes=True)