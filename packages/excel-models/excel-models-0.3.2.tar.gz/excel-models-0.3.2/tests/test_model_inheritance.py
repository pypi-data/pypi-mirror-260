import pytest

from excel_models.columns import Column
from excel_models.db import ExcelDB
from excel_models.models import ExcelModel


class UserBase(ExcelModel):
    id = Column()


class User(UserBase):
    name = Column()


class MyDB(ExcelDB):
    users = User.as_table()


@pytest.fixture()
def db(tmp_excel_file):
    return MyDB(tmp_excel_file)


def test_model_columns():
    assert len(User.column_defs) == 2
    assert [column_def.name for column_def in User.column_defs] == ['id', 'name']


def test_get_by_row(db, tmp_excel_data):
    assert db.users[0].id == tmp_excel_data[0][0]
    assert db.users[0].name == tmp_excel_data[0][1]


def test_get_by_col(db, tmp_excel_data):
    assert db.users.id[1] == tmp_excel_data[1][0]
    assert db.users.name[1] == tmp_excel_data[1][1]


def test_set_by_row(db):
    db.users[2].id = 100
    assert db.users.cell(4, 1).value == 100
    db.users[2].name = 'Chris'
    assert db.users.cell(4, 2).value == 'Chris'


def test_set_by_col(db):
    db.users.id[:2] = 50, 51
    assert db.users.cell(2, 1).value == 50
    assert db.users.cell(3, 1).value == 51
    db.users.name[3] = 'Lucy'
    assert db.users.cell(5, 2).value == 'Lucy'
