import pytest
from datetime import datetime
from unittest.mock import Mock, MagicMock

from defer import return_value

from modules.Employee import Employee

mock = Mock()
employee = Employee()

@pytest.fixture
def records():
    #id = 101
    name = "Rahul"
    lastname = "Kumar"
    join_date = datetime(2020, 9, 8)
    experience_years = 5
    records = [id,name, lastname, join_date, experience_years]
    return records

def test_insert(records):
    assert employee.insert_table_values(records[1], records[2], records[3], records[4]) == records[1]

def test_delete():
    employee.delete_record = MagicMock(return_value(1))
    assert employee.delete_record == 1
def test_update():
    assert employee.update_record(1,5) == 1


