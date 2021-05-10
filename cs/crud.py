from sqlalchemy.orm import Session

from cs import models, schemas


def create_students(db: Session, students: schemas.CreateStudents):
    db_students = models.Students(**students.dict())
    db.add(db_students)
    db.commit()
    db.refresh(db_students)
    return db_students


def create_teachers(db: Session, teachers: schemas.CreateTeachers):
    db_teachers = models.Teachers(**teachers.dict())
    db.add(db_teachers)
    db.commit()
    db.refresh(db_teachers)
    return db_teachers


def create_sections(db: Session, sections: schemas.CreateSections):
    db_sections = models.Sections(**sections.dict())
    db.add(db_sections)
    db.commit()
    db.refresh(db_sections)
    return db_sections


def create_activities(db: Session, activities: schemas.CreateActivities):
    db_activities = models.Activities(**activities.dict())
    db.add(db_activities)
    db.commit()
    db.refresh(db_activities)
    return db_activities


def create_rotary_situation(db: Session, rotary_situation: schemas.CreateRotary_situation,
                            sections_id: int, teachers_id: int, students_id: int):
    db_rotary_situation = models.Rotary_situation(**rotary_situation.dict(),
                                                  sections_id=sections_id,
                                                  teachers_id=teachers_id,
                                                  students_id=students_id)
    db.add(db_rotary_situation)
    db.commit()
    db.refresh(db_rotary_situation)
    return db_rotary_situation


def get_student_by_account(db: Session, account: str):
    return db.query(models.Students).filter(models.Students.account == account).first()


def get_teacher_by_account(db: Session, account: str):
    return db.query(models.Teachers).filter(models.Teachers.account == account).first()


def get_sections_by_name(db: Session, name: str):
    return db.query(models.Sections).filter(models.Sections.name == name).first()


# def get_activities_by_name(db: Session, name: str):
#     return db.query(models.Activities).filter(models.Activities.name == name).first()


def get_students(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Students).offset(skip).limit(limit).all()

#
# def get_city(db: Session, city_id: int):
#     return db.query(models.City).filter(models.City.id == city_id).first()
#
#
# def get_city_by_name(db: Session, name: str):
#     return db.query(models.City).filter(models.City.province == name).first()
#
#
# def get_cities(db: Session, skip: int = 0, limit: int = 10):
#     return db.query(models.City).offset(skip).limit(limit).all()
#
#
# def create_city(db: Session, city: schemas.CreateCity):
#     db_city = models.City(**city.dict())
#     db.add(db_city)
#     db.commit()
#     db.refresh(db_city)
#     return db_city
#
#
# def get_data(db: Session, city: str = None, skip: int = 0, limit: int = 10):
#     if city:
#         return db.query(models.Data).filter(models.Data.city.has(province=city))  # 外键关联查询，这里不是像Django ORM那样Data.city.province
#     return db.query(models.Data).offset(skip).limit(limit).all()
#
#
# def create_city_data(db: Session, data: schemas.CreateData, city_id: int):
#     db_data = models.Data(**data.dict(), city_id=city_id)
#     db.add(db_data)
#     db.commit()
#     db.refresh(db_data)
#     return db_data
