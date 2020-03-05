import sqlite3, jsonCrawler, stackoverflowCrawler

from typing import Dict, List, Tuple

# SPRINT 2 DATABASE FUNCS V


def open_database(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    database_conn = sqlite3.connect(filename, timeout=1)  # connect or create
    cursor = database_conn.cursor()  # get ready to r/w data
    return database_conn, cursor


def close_database(conn: sqlite3.Connection):
    conn.commit()  # commit changes
    conn.close()


def main():

    my_so_data = stackoverflowCrawler.get_stackoverflow_jobs_data()
    conn, cursor = open_database("my_SO_db2.sqlite")
    stackoverflowCrawler.setup_so_database(cursor)
    stackoverflowCrawler.save_so_to_database(cursor, my_so_data)
    close_database(conn)


main()
