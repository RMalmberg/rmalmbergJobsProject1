import pytest
import jobsCrawl
from typing import Dict, Tuple, List, Any
import sqlite3
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


def get_test_db() -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    testconn, testcurse = jobsCrawl.open_database()
    jobsCrawl.setup_database(testcurse)

    #jobsCrawl.save_to_database(testcurse)
    return testconn, testcurse


def test_database_creation(cursor: sqlite3.Cursor):
    get_test_db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_result = cursor.fetchall()
    jobsCrawl.close_database(cursor)
    assert table_result == ("jobs")



