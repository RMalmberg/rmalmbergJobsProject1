# create JSON file from http request
# Sprint 1
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
     cursor.execute(f"""INSERT OR IGNORE INTO jobs(id, type, url, date, company, company_url, location, title, description,\
        how_to_apply, company_logo) \
        VALUES("1097", "Full Time", "www.com", "12/22", "hello", "hello.org", "a place", "Captain", "yaargh", "online",\
         "doodle.logo")
    """)


def main():
    conn, cursor = open_database("my_db.sqlite")
    setup_database(cursor)
    save_to_database(cursor)
    close_database(conn)
    #  sprint1

    my_data = get_git_jobs_data()
    save_data_file(my_data)


main()

