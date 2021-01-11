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
    status = Column(String)
    lead_id = Column(Integer, ForeignKey('employees.id'))
    employees = relationship("EmployeeDb", back_populates="project")


EmployeeDb.project = relationship("Project", order_by = Project.pid, back_populates="employees")
Base.metadata.create_all(engine)



class Project_class(Exception):

    def insert_table_values(self, pname, status,lead_id):
        session = Session()

        insert_query = Project(pname= pname, status = status, lead_id = lead_id)
        session.add(insert_query)
        session.commit()
        session.refresh(insert_query)
        session.close()

        return insert_query.pname

    def delete_record(self, id):
        session = Session()

        rows = session.query(Project).filter(Project.pid == id).delete()
        session.commit()
        session.close()

        if rows == 0:
            return -1
        else:
            return rows

    def update_record(self, id, status):
        session = Session()

        rows = session.query(Project).filter(Project.pid == id).update({'status': status})
        session.commit()
        session.close()
        return rows

    def display(self):
        session = Session()

        result = session.query(Project).all()
        print("| Project Id | Name | Status | Employee id | ")

        for row in result:
            print("|  ",row.pid, "  | ", row.pname, "  | ", row.status, "  | ",
                  row.lead_id, " |")
        session.close()


    def project_name(self, status):
        session = Session()
        result = session.query(Project).filter(Project.status == status)
        project_name = None
        for row in result:
            print("Project Id: ", row.pid, " Project Name :", row.pname)
            project_name = row.pname
        session.close()

        return project_name

    def getChoice(self):
        print("----------Menu-------------------")
        print(" 1. Insert values into Table\n 2. Delete from Table\n "
              "3. Update Employee Project Status\n 4. Display Records\n "
              "5. Show Status wise projects\n 6. Exit")
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

    project = Project_class()
    choice = project.getChoice()
    while choice != 6:

        if choice == 1:
            records=[]

            count = int(input("How many Projects you want to enter?"))
            for i in range(0, count, 1):
                name = str(input("Enter Project name"))
                status = str(input("Enter Status (Active/Closed"))
                empid = int(input('Enter Lead Id'))
                records.append([name, status, empid])

            for i in range(0,len(records)) :

                #print(len(records))
                print(records)
                try:
                    result=project.insert_table_values(records[i][0], records[i][1], records[i][2])
                except NameError:
                    print("Error")
                else:
                    print("Inserted project :",result)

        elif choice == 2:
            try:
                id = int(input("Enter Project Id to be deleted"))
            except ValueError:
                print("Insert Valid Id(Interger)")
            else:
                result = project.delete_record(id)
                if result == 1:
                    print("deleted: ")
                else:
                    raise Exception("Record not found!!")

        elif choice == 3:
            # update
            try:
                id = int(input("Enter project Id to be updated"))
                status = input("enter status Active/Closed")

            except ValueError:
                print("Insert Valid values")
            else:
                result = project.update_record(id, status)
                if result == 1:
                    print("updated: ")
                else:
                    raise Exception("Record not found!!")


        elif choice == 4:
            project.display()
        elif choice == 5:
            status = (input("Enter status to list project"))
            project.project_name(status)
        else:
            print("Invalid option. Try again!")

        choice = project.getChoice()





