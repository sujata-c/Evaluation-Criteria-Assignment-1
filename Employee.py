
# ORM used SqlAlchemy

"""add to read me"""
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, insert, ForeignKey
from datetime import datetime

""" to interact with the database, we need to obtain its handle. 
    A session object is the handle to database."""
from sqlalchemy.orm import sessionmaker, relationship
"""Classes mapped using the Declarative system are defined in terms of 
a base class which maintains a catalog of classes and tables relative to 
that base - this is known as the declarative base class."""
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:////home/sujata/sqliteDb/assignmentNiyuj.db', echo = True)
Session = sessionmaker(bind = engine)
Base = declarative_base()


class EmployeeDb(Base):
   __tablename__ = 'employees'
   id = Column(Integer, primary_key=True)

   name = Column(String)
   lastname = Column(String)
   join_date = Column(Date)
   experience_years = Column(Integer)


class Project(Base):
    __tablename__ = 'project'
    pid = Column(Integer, primary_key=True)
    pname = Column(String)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    employees = relationship("EmployeeDb", back_populates="project")


EmployeeDb.project = relationship("Project", order_by = Project.pid, back_populates="employees")
Base.metadata.create_all(engine)


meta = MetaData()
employees = Table(
      'employees', meta,
      Column('id', Integer, primary_key=True),  # auto increment
      Column('name', String),
      Column('lastname', String),
      Column('join_date',Date),
      Column('experience_years',Integer)
     )
#meta.create_all(engine)      # create table


class Employee(Exception):

    def insert_table_values(self,id, name, lastname,join_date,experience_years):

        insert_query = EmployeeDb(id=id, name= name, lastname = lastname,
                                  join_date = join_date, experience_years = experience_years)
        session.add(insert_query)
        session.commit()
        session.refresh(insert_query)
        return insert_query.id

    def delete_record(self, id):
        session.query(EmployeeDb).filter(EmployeeDb.id == id).delete()
        result = session.commit()
        return result


    def update_record(self, id, years):
        session.query(EmployeeDb).filter(EmployeeDb.id == id).update({'experience_years': years})
        result = session.commit()
        return result

    def display(self):
        result = session.query(EmployeeDb).all()
        print("| Emp Id | Name | Lastname | Join date | Experience | ")

        for row in result:
            print("| ",row.id, " |", row.name, " |", row.lastname, " |",
                  row.join_date, " |", row.experience_years, " |")

    def project_name(self,eid):
        result = session.query(Project).filter(Project.employee_id == eid)
        for row in result:
            print(row.pid)

    def getChoice(self):
        print("----------Menu-------------------")
        print(" 1. Insert values into Table\n 2. Delete from Table\n "
              "3. Update Employee Experience years\n 4. Display Records\n "
              "5. Show project for a employee\n 6. Exit")
        try:
            choice = int(input("Enter your choice"))
        except ValueError:
            print("enter 1 to 6")
        return choice


# define Python user-defined exceptions


class InvalidOption(Exception):
    pass


class YearValueError(Exception):
    pass


class MonthValueError(Exception):
    pass



if __name__=='__main__':

    emp = Employee()
    choice = emp.getChoice()
    while choice != 6:
        session = Session()

        if choice == 1:
            records=[]

            count = int(input("How many Employees you want to enter?"))
            for i in range(0, count, 1):
                emp_info={}
                id=int(input("enter id"))
                name = str(input("Enter Employee name"))
                lastname = str(input("Enter Last name"))

                date_entry = input('Enter join date (i.e. 2017-7-1)')
                try:
                    year, month, day = map(int, date_entry.split('-'))
                    if year > 2020 or year < 1960:
                        raise YearValueError

                    if month > 12 or month <=0:
                        raise MonthValueError
                    date = datetime(year, month, day)
                    join_date = date
                except ValueError:
                    print(date)

                except YearValueError:
                    print("Invalid Year")

                except MonthValueError:
                    print("Enter Month between 1 to 12")
                except NameError:
                    print("date no valid")

                experience_years =int(input('Enter a date (i.e. 2017-7-1)'))
                emp_info={'id':id, 'name': name, 'lastname': lastname, 'join_date':join_date,
                          'experience_years':experience_years}
                records.append(emp_info)

            for i in records :

                print(len(records))
                print(records)
                ''' try:
                    result=emp.insert_table_values(id,name, lastname, join_date, experience_years)
                except NameError:
                    print("Error")
                else:
                    print("Inserted Id",result)'''

        elif choice == 2:
            try:
                id=int(input("Enter Employee Id to be deleted"))
            except ValueError:
                print("Insert Valid Id(Interger")
            result = emp.delete_record(id)

        elif choice == 3:
            # update
            try:
                id = int(input("Enter Employee Id to be updated"))
                exp_yrs = int(input("enter new experience year count"))

            except ValueError:
                print("Insert Valid values")
            result = emp.update_record(id, exp_yrs)

        elif choice == 4:
            emp.display()
        elif choice == 5:
            eid=int(input("Enter employee id whose project you want"))
            emp.project_name(eid)
        else:
            print("Invalid option. Try again!")

        session.close()
        choice = emp.getChoice()





