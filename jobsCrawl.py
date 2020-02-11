# create SQLite Database from my_data.txt

# Sprint 2
# By Raina Malmberg of 490-004

import requests
import json
import time
import sqlite3

from typing import Dict, List, Tuple


def get_git_jobs_data() -> List[Dict]:

    jobs_data = []
    page = 1
    more_data = True
    while more_data:
        url = f"https://jobs.github.com/positions.json?description=&location=&page={page}"
        raw_data = requests.get(url)

        if "GitHubber!" in raw_data:  # only happens in testing
            continue

        partial_output = raw_data.json()
        jobs_data.extend(partial_output)
        if len(partial_output) < 50:
            more_data = False
        time.sleep(.1)
        page += 1

    return jobs_data


def save_data_file(data, filename='my_data.txt'):
    with open(filename, 'a', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    return filename

# SPRINT 1 JSON FUNCS ^
# SPRINT 2 DATABASE FUNCS V


def open_database(filename: str)->Tuple[sqlite3.Connection, sqlite3.Cursor]:
    database_conn = sqlite3.connect(filename)  # connect or create
    cursor = database_conn.cursor()  # get ready to r/w data
    return database_conn, cursor


def close_database(conn: sqlite3.Connection):
    conn.commit()  # commit changes
    conn.close()


def setup_database(cursor: sqlite3.Cursor):

    cursor.execute(""" CREATE TABLE IF NOT EXISTS jobs(
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    url TEXT NOT NULL,
    created_at TEXT NOT NULL,
    date TEXT NOT NULL,
    company TEXT NOT NULL,
    company_url TEXT NOT NULL,
    location TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    how_to_apply TEXT NOT NULL,
    company_logo TEXT NOT NULL
    );""")


def save_to_database(cursor: sqlite3.Cursor):

        cursor.execute(f"""INSERT OR IGNORE INTO jobs(id, type, url, created_at, date, company, company_url, location, title, description,\
                how_to_apply, company_logo) \
                VALUES("1234", "Full Time", "www.com", DATE ('now'), "12/22", "hello", "hello.org", "a place", "Captain", "yaargh",\
                 "online", "doodle.logo")""")


def get_table_from_database(cursor: sqlite3.Cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_result = cursor.fetchall()
    print(table_result)
    return table_result


def get_jobs_dict_keys(json_data):
        got_keys = False
        for dict in json_data:
            keys = dict.keys()
            while got_keys == False:
                with open("keys.txt", 'a', encoding='utf-8') as file:
                    file.write(str(keys))
                    got_keys = True
        return keys


def get_keys_as_list(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        key_list = file.readlines()
        file.close()
    return key_list


def get_jobs_dict_values(json_data):
    for dict in json_data:
        val = dict.values()
        with open("values.txt", 'a', encoding='utf-8') as file:
            file.write(str(val))
            file.write("\n")
    print(type(val))
    return val


def main():
    my_data = get_git_jobs_data()
    save_data_file(my_data)
    get_jobs_dict_keys(my_data)
    conn, cursor = open_database("my_db.sqlite")
    setup_database(cursor)
    # saves dummy data to my_db.sqlite
    save_to_database(cursor)
    # gets table name from my_db.sqlite
    get_table_from_database(cursor)

    close_database(conn)
   # my_keys = get_keys_as_list('keys.txt')

main()
