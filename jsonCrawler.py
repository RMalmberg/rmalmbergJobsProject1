# create SQLite Database from Stack Overflow RSS feed

# Sprint 3
# By Raina Malmberg of 490-004

import requests
import json
import time
import sqlite3
import jobsDB, stackoverflowCrawler

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


def save_git_to_database(cursor: sqlite3.Cursor, jobs_data):
    insert_job_info_statement = f"""INSERT INTO github_jobs VALUES (?,?,?,?,?, ?,?,?,?)"""

    for job_info in jobs_data:

        # get job_info values from each dict to insert into our sqlite db
        info_to_save = tuple(job_info.values())
        cursor.execute(insert_job_info_statement, info_to_save)


def setup_git_database(cursor: sqlite3.Cursor):
    cursor.execute(""" CREATE TABLE github_jobs(
        id TEXT PRIMARY KEY,
        type TEXT,
        url TEXT,
        published TEXT,
        company TEXT,
        company_url TEXT,
        location TEXT,
        title TEXT,
        description TEXT
        );""")

# SPRINT 1 JSON FUNCS ^


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


# SPRINT 3 HTML/XML PARSER FUNCS V


# Sprint 1 & 2 commands
# my_data = get_git_jobs_data()
# save_data_file(my_data)

# conn, cursor = open_database("my_db.sqlite")
# setup_database(cursor)

# save_git_to_database(cursor, my_data)
# close_database(conn)


