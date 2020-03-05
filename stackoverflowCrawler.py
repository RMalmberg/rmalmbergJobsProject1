import sqlite3
import feedparser
from pprint import pprint as ppr

def feedparser_fun():
    feed = feedparser.parse("https://stackoverflow.com/jobs/feed")
    entries = feed.entries
    print(entries[150].published)


def get_stackoverflow_jobs_data():
    #
    feed = feedparser.parse("https://stackoverflow.com/jobs/feed")

    entries = feed.entries

    return entries

# Sprint 3
def setup_so_database(cursor: sqlite3.Cursor):
    cursor.execute(""" CREATE TABLE stack_overflow_jobs(
        id TEXT NOT NULL PRIMARY KEY,
        category TEXT NOT NULL,
        url TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL
        );""")


def save_so_to_database(cursor: sqlite3.Cursor, stack_data):

    insert_statement = f"""INSERT OR IGNORE INTO jobs_api_data (id, link, url, description) VALUES (?,?,?, ?,?)"""
    for job_info in stack_data:
        # populate rows for all jobs
        cursor.execute(insert_statement, [job_info['id'],  job_info['link'],
                                          job_info['title'], job_info['description'],
                                          ])

# job_info['category'],
# Sprint 3 Testing funcs


def create_test_table(cursor: sqlite3.Cursor):
    cursor.execute(""" CREATE TABLE SO_Test(
        id text NOT NULL PRIMARY KEY
    );""")


def pop_test_table(cursor: sqlite3.Cursor, stack_data):
    for job_info in stack_data:
        cursor.execute("""INSERT INTO SO_Test VALUES (?)""", [job_info['id']])

#company_url NULL,
        #location NULL,

if __name__ == '__main__':
    feedparser_fun()
