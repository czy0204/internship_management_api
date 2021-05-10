from datetime import date
from datetime import datetime

from pydantic import BaseModel


class CreateAdmins(BaseModel):
    account: str
    pwd: str = '123'


class CreateTeachers(BaseModel):
    account: str
    pwd: str = '123'
    phone: str
    email: str


class CreateStudents(BaseModel):
    account: str
    pwd: str = '123'
    name: str
    gender: str
    graduation_school: str
    phone: str
    email: str
    status: str = '未审核'


class CreateSections(BaseModel):
    name: str


class CreateActivities(BaseModel):
    name: str
    time: str
    location: str
    details: str


class CreateLeaves(BaseModel):
    leaves_time: datetime
    reason: str
    teachers_options: str
    admins_options: str


class CreateActivities_registration(BaseModel):
    pass


class CreateAbsence_information(BaseModel):
    pass


class CreateRotary_situation(BaseModel):
    time: date
    end_time: date
    students_to_teachers: str
    teachers_to_students: str
    achievements: str


class ReadAdmins(CreateAdmins):
    id: int

    class Config:
        orm_mode = True


class ReadTeachers(CreateTeachers):
    id: int

    class Config:
        orm_mode = True


class ReadStudents(CreateStudents):
    id: int

    class Config:
        orm_mode = True


class ReadSections(CreateSections):
    id: int

    class Config:
        orm_mode = True


class ReadActivities(CreateActivities):
    id: int

    class Config:
        orm_mode = True


class ReadLeaves(CreateLeaves):
    id: int
    students_id: int
    updated_time: datetime

    class Config:
        orm_mode = True


class ReadActivities_registration(CreateActivities_registration):
    id: int
    students_id: int
    activities_id: int

    class Config:
        orm_mode = True


class ReadAbsence_information(CreateAbsence_information):
    id: int
    teachers_id: int
    students_id: int
    created_time: datetime

    class Config:
        orm_mode = True


class ReadRotary_situation(CreateRotary_situation):
    id: int
    sections_id: int
    teachers_id: int
    students_id: int

    class Config:
        orm_mode = True





