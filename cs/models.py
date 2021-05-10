from sqlalchemy import Column, String, Integer, BigInteger, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from .database import Base


class Admins(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    account = Column(String(32), unique=True, nullable=False, comment='账号')
    pwd = Column(String(32), default='123', nullable=False, comment='密码')


class Teachers(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    account = Column(String(32), unique=True, nullable=False, comment='账号')
    pwd = Column(String(32), default='123', nullable=False, comment='密码')
    phone = Column(String(32), comment='联系电话')
    email = Column(String(32), comment='邮箱')

    absence_information = relationship('Absence_information', back_populates='teachers')
    rotary_situation = relationship('Rotary_situation', back_populates='teachers')


class Students(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    account = Column(String(32), unique=True, nullable=False, comment='账号/学号')
    pwd = Column(String(32), default='123', nullable=False, comment='密码')
    name = Column(String(32), nullable=False, comment='姓名')
    gender = Column(String(32), nullable=False, comment='性别')
    graduation_school = Column(String(32), nullable=False, comment='毕业院校')
    phone = Column(String(32), comment='联系电话')
    email = Column(String(32), comment='邮箱')
    status = Column(String(32), default='未审核', comment='审核状态')

    leaves = relationship('Leaves', back_populates='students')
    activities_registration = relationship('Activities_registration', back_populates='students')
    absence_information = relationship('Absence_information', back_populates='students')
    rotary_situation = relationship('Rotary_situation', back_populates='students')


class Sections(Base):
    __tablename__ = 'sections'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(32), nullable=False, comment='科室名称')

    rotary_situation = relationship('Rotary_situation', back_populates='sections')


class Activities(Base):
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(32), nullable=False, comment='活动名称')
    time = Column(String(32), nullable=False, comment='活动时间')
    location = Column(String(32), nullable=False, comment='活动地点')
    details = Column(String(1000), nullable=False, comment='活动详情')

    activities_registration = relationship('Activities_registration', back_populates='activities')


class Leaves(Base):
    __tablename__ = 'leaves'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    students_id = Column(Integer, ForeignKey('students.id'), comment='学生id')
    leaves_time = Column(DateTime, nullable=False, comment='请假时间')
    reason = Column(String(100), nullable=False, comment='请假理由')
    teachers_options = Column(String(100), comment='导师审核意见')
    admins_options = Column(String(100), comment='管理员审核意见')
    updated_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    students = relationship('Students', back_populates='leaves')


class Activities_registration(Base):
    __tablename__ = 'activities_registration'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    students_id = Column(Integer, ForeignKey('students.id'), comment='学生id')
    activities_id = Column(Integer, ForeignKey('activities.id'), comment='活动id')

    students = relationship('Students', back_populates='activities_registration')
    activities = relationship('Activities', back_populates='activities_registration')


class Absence_information(Base):
    __tablename__ = 'absence_information'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    teachers_id = Column(Integer, ForeignKey('teachers.id'), comment='教师id')
    students_id = Column(Integer, ForeignKey('students.id'), comment='学生id')
    created_time = Column(DateTime, server_default=func.now(), comment='创建时间')

    teachers = relationship('Teachers', back_populates='absence_information')
    students = relationship('Students', back_populates='absence_information')


class Rotary_situation(Base):
    __tablename__ = 'rotary_situation'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sections_id = Column(Integer, ForeignKey('sections.id'), comment='科室id')
    teachers_id = Column(Integer, ForeignKey('teachers.id'), comment='教师id')
    students_id = Column(Integer, ForeignKey('students.id'), comment='学生id')
    time = Column(Date, comment='轮转开始时间')
    end_time = Column(Date, comment='轮转结束时间')
    students_to_teachers = Column(String(100), comment='学生评价老师')
    teachers_to_students = Column(String(100), comment='老师评价学生')
    achievements = Column(String(100), comment='成绩')  # 未完善

    sections = relationship('Sections', back_populates='rotary_situation')
    teachers = relationship('Teachers', back_populates='rotary_situation')
    students = relationship('Students', back_populates='rotary_situation')


# class City(Base):
#     __tablename__ = 'city'  # 数据表的表名
#
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     province = Column(String(100), unique=True, nullable=False, comment='省/直辖市')
#     country = Column(String(100), nullable=False, comment='国家')
#     country_code = Column(String(100), nullable=False, comment='国家代码')
#     country_population = Column(BigInteger, nullable=False, comment='国家人口')
#     data = relationship('Data', back_populates='city')  # 'Data'是关联的类名；back_populates来指定反向访问的属性名称
#
#     created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
#     updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')
#
#     __mapper_args__ = {"order_by": country_code}  # 默认是正序，倒序加上.desc()方法
#
#     def __repr__(self):
#         return f'{self.country}_{self.province}'
#
#
# class Data(Base):
#     __tablename__ = 'data'
#
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     city_id = Column(Integer, ForeignKey('city.id'), comment='所属省/直辖市')  # ForeignKey里的字符串格式不是类名.属性名，而是表名.字段名
#     date = Column(Date, nullable=False, comment='数据日期')
#     confirmed = Column(BigInteger, default=0, nullable=False, comment='确诊数量')
#     deaths = Column(BigInteger, default=0, nullable=False, comment='死亡数量')
#     recovered = Column(BigInteger, default=0, nullable=False, comment='痊愈数量')
#     city = relationship('City', back_populates='data')  # 'City'是关联的类名；back_populates来指定反向访问的属性名称
#
#     created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
#     updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')
#
#     __mapper_args__ = {"order_by": date.desc()}  # 按日期降序排列
#
#     def __repr__(self):
#         return f'{repr(self.date)}：确诊{self.confirmed}例'


""" 附上三个SQLAlchemy教程

SQLAlchemy的基本操作大全 
    http://www.taodudu.cc/news/show-175725.html

Python3+SQLAlchemy+Sqlite3实现ORM教程 
    https://www.cnblogs.com/jiangxiaobo/p/12350561.html

SQLAlchemy基础知识 Autoflush和Autocommit
    https://zhuanlan.zhihu.com/p/48994990
"""
