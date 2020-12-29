
# ORM used SqlAlchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date
from datetime import datetime


engine = create_engine('sqlite:////home/sujata/sqliteDb/assignmentNiyuj.db', echo = True)
print(engine)
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
        insert = employees.insert().values(id=id, name=name, lastname=lastname)
        conn=engine.connect()
        result=conn.execute(insert)

        return result.inserted_primary_key

# define Python user-defined exceptions


class InvalidOption(Exception):
    pass


class YearValueError(Exception):
    pass


class MonthValueError(Exception):
    pass


if __name__=='__main__':

    emp = Employee()

    print("----------Menu-------------------")
    print(" 1. Insert values into Table\n 2. Delete from Table\n 3. Update Record\n 4. Display Records\n "
            "5. Show project wise employees\n 6. Exit")
    try:
        choice = int(input("Enter your choice"))
        if choice > 6 or choice <= 0:
            raise InvalidOption
    except InvalidOption:
        print("Enter valid option")
    except ValueError:
        print("Enter between 1 to 6")


    if choice == 6:
        exit()

    if choice == 1:
        count = int(input("How many Employees you want to enter?"))
        for i in range(0, count, 1):
            id=int(input("enter id"))
            name = str(input("Enter Employee name"))
            lastname = str(input("Enter Last name"))

            date_entry = input('Enter a date (i.e. 2017-7-1)')
            try:
                year, month, day = map(int, date_entry.split('-'))
                if year > 2020 or year < 1960:
                    raise YearValueError

                if month > 12 or month <=0:
                    raise MonthValueError
                date = datetime(year, month, day)
            except ValueError:
                print(date)
                break
            except YearValueError:
                print("Invalid Year")
                break
            except MonthValueError:
                print("Enter Month between 1 to 12")
                break

            join_date=date
            experience_years = 2

        for i in range(0, count, 1):
            result=emp.insert_table_values(id,name, lastname, join_date, experience_years)
            print("Inserted Id",result)

    #if choice == 2:





