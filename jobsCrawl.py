# create SQLite Database from Stack Overflow RSS feed

# Sprint 3
# By Raina Malmberg of 490-004

import requests
import json
import time
import sqlite3
import feedparser

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


def open_database(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    database_conn = sqlite3.connect(filename)  # connect or create
    cursor = database_conn.cursor()  # get ready to r/w data
    return database_conn, cursor


def close_database(conn: sqlite3.Connection):
    conn.commit()  # commit changes
    conn.close()


def setup_database(cursor: sqlite3.Cursor):
    cursor.execute(""" CREATE TABLE github_jobs(
        id TEXT PRIMARY KEY,
        type TEXT,
        url TEXT,
        created_at TEXT,
        company TEXT,
        company_url TEXT,
        location TEXT,
        title TEXT,
        description TEXT,
        how_to_apply TEXT,
        company_logo TEXT
        );""")


def save_git_to_database(cursor: sqlite3.Cursor, jobs_data):
    insert_job_info_statement = f"""INSERT INTO github_jobs VALUES (?,?,?,?,?, ?,?,?,?,?, ?)"""

    for job_info in jobs_data:

        # get job_info values from each dict to insert into our sqlite db
        info_to_save = tuple(job_info.values())
        cursor.execute(insert_job_info_statement, info_to_save)


def setup_test_table(cursor: sqlite3.Cursor):
    cursor.execute(f"""INSERT INTO github_jobs VALUES ('1234','Part-Time','www.job.com', '1-1-1111', 'DreamCorps',
        'dreamcorp.com', 'Hades', 'Software Engineer', 'Best job and company of Year 1111', 'online','logo-url') """)


# practice
    """"
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


def get_table_from_database(cursor: sqlite3.Cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_result = cursor.fetchall()
    print(table_result)
    return table_result


def get_jobs_dict_keys(json_data):
    got_keys = False
    for dict in json_data:
        keys = dict.keys()
        while not got_keys:
            with open("keys.txt", 'a', encoding='utf-8') as file:
                file.write(str(keys))
                got_keys = True
    return keys
    """

# SPRINT 2 FUNCS ^
# SPRINT 3 HTML/XML PARSER FUNCS V


def feedparser_fun():
    feed = feedparser.parse("https://stackoverflow.com/jobs/feed")
    print(feed.entries[1].id)


def get_stackoverflow_jobs_data():

    feed = feedparser.parse("https://stackoverflow.com/jobs/feed")

    entries = feed.entries

    return entries


def setup_so_database(cursor: sqlite3.Cursor):
    cursor.execute(""" CREATE TABLE stackoverflow_jobs(
        id TEXT NOT NULL PRIMARY KEY,
        title TEXT NOT NULL,
        link TEXT NOT NULL,
        description TEXT NOT NULL,
        category TEXT NOT NULL
        );""")


def save_so_to_database(cursor: sqlite3.Cursor, stack_data):
    insert_statement = f"""INSERT INTO stackoverflow_jobs VALUES (?, ?, ?, ?, ?)"""
    for job_info in stack_data:
        # get job_info values from each key to insert into our sqlite db for SO
        cursor.execute(insert_statement, [job_info['id'], job_info['title'], job_info['link'], job_info['description'],
                                          job_info['category']])

# Sprint 3 Testing funcs


def create_test_table(cursor: sqlite3.Cursor):
    cursor.execute(""" CREATE TABLE SO_Test(
        id text NOT NULL PRIMARY KEY
    );""")


def pop_test_table(cursor: sqlite3.Cursor, stack_data):
    for job_info in stack_data:
        cursor.execute("""INSERT INTO SO_Test VALUES (?)""", [job_info['id']])


def main():
    my_so_data = get_stackoverflow_jobs_data()
    conn, cursor = open_database("my_SO_db.sqlite")
    setup_so_database(cursor)
    save_so_to_database(cursor, my_so_data)
    close_database(conn)

# Sprint 1 & 2 commands
# my_data = get_git_jobs_data()
# save_data_file(my_data)

# conn, cursor = open_database("my_db.sqlite")
# setup_database(cursor)

# save_git_to_database(cursor, my_data)
# close_database(conn)


main()
