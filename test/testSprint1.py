import sqlite3
import jobsCrawl
import pytest
from typing import Dict, List, Tuple

@pytest.fixture
def get_data():
    import jobsCrawl
    return jobsCrawl.get_git_jobs_data()




def test_jobs_dict(get_data):
    # test 1
    assert len(get_data) >= 150
    assert type(get_data[1]) is dict


def test_is_job_there():
    found = False
    with open('../my_data.txt', encoding='utf-8') as datafile:
        data = datafile.readlines()
        for line in data:
            print(line)
            if "Senior Full Stack" in line:
                found = True
    assert  found == True


def test_job_in_data(get_data):
    data = get_data
    fulltime = False
    contract = False
    for i in data:
        if i['type'] == 'Contract':
            contract = True
        if i['type'] == 'Full Time':
            fulltime = True
    assert contract and fulltime


# Sprint 2 #

def test_dictionary_values(get_data):
    got_keys = False
    for dict in get_data:
        keys = dict.keys()
        while got_keys == False:
            with open("keys.txt", 'a', encoding='utf-8') as file:
                file.write(str(keys))
                got_keys = True

    got_vals = False
    for dict in get_data:
        val = dict.values()
        with open("values.txt", 'a', encoding='utf-8') as file:
            file.write(str(val))
            file.write("\n")
            got_vals = True

    assert got_keys and got_vals

# attempt at db test
def get_test_db()->Tuple[sqlite3.Connection, sqlite3.Cursor]:

    testconn, testcurse= jobsCrawl.open_database()
    jobsCrawl.setup_database(testcurse)

    #jobsCrawl.save_to_database(testcurse)
    return testconn, testcurse


def test_database_creation(cursor: sqlite3.Cursor):
    get_test_db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_result = cursor.fetchall()
    jobsCrawl.close_database(cursor)
    assert table_result == ("jobs")




    """
def test_save_txt():
    # required test 2
    some_data = {'id': 1232, 'type': "Testable"}
    list_data = []
    list_data.append(some_data)
    filename = "my_data.txt"
    jobsCrawl.save_data_file(list_data, filename)
    test_file = open(filename, 'r')
    save_data = test_file.readlines()
    # saves extra lines to txt
    #assert f"{str(some_data)}\n" in save_data
    """