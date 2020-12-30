from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, insert, ForeignKey
from datetime import datetime

""" to interact with the database, we need to obtain its handle. 
    A session object is the handle to database."""
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from Employee import EmployeeDb as ed


engine = create_engine('sqlite:////home/sujata/sqliteDb/assignmentNiyuj.db', echo = True)
Session = sessionmaker(bind = engine)
Base = declarative_base()
session=Session()


class Project(Base):
    __tablename__ = 'project'
    pid = Column(Integer, primary_key=True)
    pname = Column(String)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    customer = relationship("ed", back_populates="project")


ed.invoices = relationship("Project", order_by = Project.pid, back_populates="customer")
# Base.metadata.create_all(engine)

result=session.query(Project, ed).filter(Project.pid == 1)
for row in result:
    print(row.pid,"  ", row.pname)
