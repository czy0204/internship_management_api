from typing import List

import requests
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request

from pydantic import HttpUrl
from sqlalchemy.orm import Session

from cs import crud, schemas
from cs.database import engine, Base, SessionLocal
from cs.models import Admins, Teachers, Students, Sections, Activities, Leaves, Activities_registration, Absence_information, Rotary_situation

application = APIRouter()


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@application.post("/create_students", response_model=schemas.ReadStudents)
def create_students(student: schemas.CreateStudents, db: Session = Depends(get_db)):
    db_students = crud.get_student_by_account(db, account=student.account)
    if db_students:
        raise HTTPException(status_code=400, detail="Student already registered")
    return crud.create_students(db=db, students=student)


@application.post("/create_teachers", response_model=schemas.ReadTeachers)
def create_teachers(teachers: schemas.CreateTeachers, db: Session = Depends(get_db)):
    db_teachers = crud.get_teacher_by_account(db, account=teachers.account)
    if db_teachers:
        raise HTTPException(status_code=400, detail="Student already registered")
    return crud.create_teachers(db=db, teachers=teachers)


@application.post("/create_sections", response_model=schemas.ReadSections)
def create_sections(sections: schemas.CreateSections, db: Session = Depends(get_db)):
    db_sections = crud.get_sections_by_name(db, name=sections.name)
    if db_sections:
        raise HTTPException(status_code=400, detail="Section already registered")
    return crud.create_sections(db=db, sections=sections)


@application.post("/create_activities", response_model=schemas.ReadActivities)
def create_activities(activities: schemas.CreateActivities, db: Session = Depends(get_db)):
    # db_activities = crud.get_activities_by_name(db, name=activities.name)
    # if db_activities:
    #     raise HTTPException(status_code=400, detail="Active already registered")
    return crud.create_activities(db=db, activities=activities)


@application.post("/create_rotary_situation", response_model=schemas.CreateRotary_situation)
def create_rotary_situation(sections: str, teachers_account: str, students_account: str, rotary_situation: schemas.CreateRotary_situation, db: Session = Depends(get_db)):
    db_students = crud.get_student_by_account(db=db, account=students_account)
    db_teachers = crud.get_teacher_by_account(db=db, account=teachers_account)
    db_sections = crud.get_sections_by_name(db=db, name=sections)
    if not db_students:
        raise HTTPException(status_code=400, detail="学生不存在")
    if not db_teachers:
        raise HTTPException(status_code=400, detail="老师不存在")
    if not db_sections:
        raise HTTPException(status_code=400, detail="科室不存在")
    return crud.create_rotary_situation(db=db, rotary_situation=rotary_situation, sections_id=db_sections.id, teachers_id=db_teachers.id, students_id=db_students.id)


@application.get("/get_student/{account}", response_model=schemas.ReadStudents)
def get_student(account: str, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_account(db, account=account)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@application.get("/get_students", response_model=List[schemas.ReadStudents])
def get_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cities = crud.get_students(db, skip=skip, limit=limit)
    return cities


#
#
# @application.post("/create_city", response_model=schemas.ReadCity)
# def create_city(city: schemas.CreateCity, db: Session = Depends(get_db)):
#     db_city = crud.get_city_by_name(db, name=city.province)
#     if db_city:
#         raise HTTPException(status_code=400, detail="City already registered")
#     return crud.create_city(db=db, city=city)
#
#
# @application.get("/get_city/{city}", response_model=schemas.ReadCity)
# def get_city(city: str, db: Session = Depends(get_db)):
#     db_city = crud.get_city_by_name(db, name=city)
#     if db_city is None:
#         raise HTTPException(status_code=404, detail="City not found")
#     return db_city
#
#
# @application.get("/get_cities", response_model=List[schemas.ReadCity])
# def get_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     cities = crud.get_cities(db, skip=skip, limit=limit)
#     return cities
#
#
# @application.post("/create_data", response_model=schemas.ReadData)
# def create_data_for_city(city: str, data: schemas.CreateData, db: Session = Depends(get_db)):
#     db_city = crud.get_city_by_name(db, name=city)
#     data = crud.create_city_data(db=db, data=data, city_id=db_city.id)
#     return data
#
#
# @application.get("/get_data")
# def get_data(city: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     data = crud.get_data(db, city=city, skip=skip, limit=limit)
#     return data
#
#
# def bg_task(url: HttpUrl, db: Session):
#     """这里注意一个坑，不要在后台任务的参数中db: Session = Depends(get_db)这样导入依赖"""
#
#     city_data = requests.get(url=f"{url}?source=jhu&country_code=CN&timelines=false")
#
#     if 200 == city_data.status_code:
#         db.query(City).delete()  # 同步数据前先清空原有的数据
#         for location in city_data.json()["locations"]:
#             city = {
#                 "province": location["province"],
#                 "country": location["country"],
#                 "country_code": "CN",
#                 "country_population": location["country_population"]
#             }
#             crud.create_city(db=db, city=schemas.CreateCity(**city))
#
#     coronavirus_data = requests.get(url=f"{url}?source=jhu&country_code=CN&timelines=true")
#
#     if 200 == coronavirus_data.status_code:
#         db.query(Data).delete()
#         for city in coronavirus_data.json()["locations"]:
#             db_city = crud.get_city_by_name(db=db, name=city["province"])
#             for date, confirmed in city["timelines"]["confirmed"]["timeline"].items():
#                 data = {
#                     "date": date.split("T")[0],  # 把'2020-12-31T00:00:00Z' 变成 ‘2020-12-31’
#                     "confirmed": confirmed,
#                     "deaths": city["timelines"]["deaths"]["timeline"][date],
#                     "recovered": 0  # 每个城市每天有多少人痊愈，这种数据没有
#                 }
#                 # 这个city_id是city表中的主键ID，不是coronavirus_data数据里的ID
#                 crud.create_city_data(db=db, data=schemas.CreateData(**data), city_id=db_city.id)
#
#
# @application.get("/sync_coronavirus_data/jhu")
# def sync_coronavirus_data(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
#     """从Johns Hopkins University同步COVID-19数据"""
#     background_tasks.add_task(bg_task, "https://coronavirus-tracker-api.herokuapp.com/v2/locations", db)
#     return {"message": "正在后台同步数据..."}
#
#
# @application.get("/")
# def coronavirus(request: Request, city: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     data = crud.get_data(db, city=city, skip=skip, limit=limit)
#     return templates.TemplateResponse("home.html", {
#         "request": request,
#         "data": data,
#         "sync_data_url": "/coronavirus/sync_coronavirus_data/jhu"
#     })
