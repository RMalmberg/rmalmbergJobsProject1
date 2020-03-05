import requests
import time
import sqlite3
import feedparser
import pandas
import sqlalchemy as sa
import geopy
from typing import Dict, List, Tuple


# database functions
def open_database(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    database_conn = sqlite3.connect(filename, timeout=1)  # connect or create
    cursor = database_conn.cursor()  # get ready to r/w data
    return database_conn, cursor


def close_database(conn: sqlite3.Connection):
    conn.commit()  # commit changes
    conn.close()


# create one table function
def setup_database(cursor: sqlite3.Cursor):
    cursor.execute(""" CREATE TABLE jobs_api_data(
        id TEXT PRIMARY KEY,
        type TEXT,
        url TEXT,
        published TEXT,
        company TEXT,
        company_url TEXT,
        location TEXT,
        title TEXT,
        description TEXT,
        apply TEXT,
        company_logo TEXT
        );""")


# json processing
def get_git_jobs_data() -> List[Dict]:
    jobs_data = []
    page = 1
    more_data = True
    while more_data:
        url = f"https://jobs.github.com/positions.json?description=&location=&page={page}"
        raw_data = requests.get(url)

        if "GitHubber!" in raw_data:  # only happens in testing
            continue
        if 'json' in raw_data.headers.get('Content-Type'):
            partial_output = raw_data.json()
            jobs_data.extend(partial_output)
            if len(partial_output) < 50:
                more_data = False
        else:
            print("data is not in json format")
        time.sleep(.1)
        page += 1

    return jobs_data


def save_git_to_database(cursor: sqlite3.Cursor, jobs_data):
    insert_job_info_statement = f"""INSERT OR IGNORE INTO jobs_api_data VALUES (?,?,?,?,?, ?,?,?,?,?, ?)"""

    for job_info in jobs_data:
        # save job info to table
        info_to_save = tuple(job_info.values())
        cursor.execute(insert_job_info_statement, info_to_save)


# stack overflow xml processing
def get_stack_overflow_jobs_data():
    #
    feed = feedparser.parse("https://stackoverflow.com/jobs/feed")

    entries = feed.entries

    return entries


def save_so_to_database(cursor: sqlite3.Cursor, stack_data):

    insert_statement = f"""INSERT OR IGNORE INTO jobs_api_data (id, url, title, description) VALUES (?,?,?,?)"""
    for job_info in stack_data:
        # populate rows for all jobs
        cursor.execute(insert_statement, [job_info['id'],  job_info['link'],
                                          job_info['title'], job_info['description']
                                          ])


def establish_pandas_engine():
    engine = sa.create_engine('sqlite:///my_db4.sqlite')
    df = pandas.read_sql_table("jobs_api_data", engine, columns=['location'])
    print(df)
    
# now we have the locations for every job that has a locate in the db.
# next: use geopy to reverse location name into coords
# create new coords table and populate lat and long with the returned list of coords, liost of dicts?
# use pandas dataframe on coords table to plot chart data with the rest of the data from jobs api data


def main():
    my_git_data = get_git_jobs_data()
    my_so_data = get_stack_overflow_jobs_data()
    conn, cursor = open_database("my_db4.sqlite")
    setup_database(cursor)
    save_git_to_database(cursor, my_git_data)
    save_so_to_database(cursor, my_so_data)
   # establish_pandas_engine()
    close_database(conn)


def main2():
    establish_pandas_engine()

#main()
main2()