import requests
import time
import sqlite3
import feedparser
import pandas
import sqlalchemy as sa
import geotext as gt
import plotly.graph_objects as go

from geopy.geocoders import Nominatim
from typing import Dict, List, Tuple


# database functions
# opens .db file
def open_database(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    database_conn = sqlite3.connect(filename, timeout=1)  # connect or create
    cursor = database_conn.cursor()  # get ready to r/w data
    return database_conn, cursor


# closes .db file
def close_database(conn: sqlite3.Connection):
    conn.commit()  # commit changes
    conn.close()


# create one table function for git and stack api data
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


# saves git data into jobs_api_data
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


# saves stack overflow data into jobs api data
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
    return df


# now we have the locations for every job that has a locate in the db.
# next: use geopy to reverse location name into coords
# create new coords table and populate lat and long with the returned list of coords, liost of dicts?
# use pandas dataframe on coords table to plot chart data with the rest of the data from jobs api data

def convert_location_to_coords_git(cursor: sqlite3.Cursor, location_data):
    geolocator = Nominatim(user_agent="my geo agent")
    for job in location_data:
        loc = geolocator.geocode(job["location"], timeout=15)
        if loc == ("remote" or "Remote") or loc is None:
            print("No location provided")
            continue
        else:
            job_loc = job['location']
            job_lat = loc.latitude
            job_long = loc.longitude
            job_id = job['id']
        cursor.execute(f'''INSERT INTO coords_of_jobs(id, location, latitude, longitude) VALUES (?,?,?,?)''',
                       (job_id, job_loc, job_lat, job_long))


# get stack overflow coords
def convert_location_to_coords_so(cursor: sqlite3.Cursor, location_data):
    geolocator = Nominatim(user_agent="my geo_so agent")
    for job in location_data:
        places = gt.GeoText(job['description'])
        loc = geolocator.geocode(places.cities)
        if loc == ("remote" or "Remote") or loc is None:
            print("No location provided")
            continue
        else:
            job_lat = loc.latitude
            job_long = loc.latitude
            job_id = job['id']
    cursor.execute(f'''INSERT INTO coords_of_jobs(id, latitude, longitude) VALUES (?,?,?)''',
                   (job_id, job_lat, job_long))


# prepares empty table for coords
def create_coords_table(cursor: sqlite3.Cursor):
    cursor.execute("""CREATE TABLE coords_of_jobs(
        id TEXT PRIMARY KEY,
        location NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL
        );""")


# requires git jobs api saved to a database
# queries our two tables for results on the map
def scatter_map():
    conn = sqlite3.connect("my_db4.sqlite", timeout=2)
    git_df = pandas.read_sql_query("SELECT * FROM jobs_api_data", conn)
    git_df['text'] = git_df['title'] + " at " + git_df['company'] + " in " + git_df['location']
    coords_df = pandas.read_sql_query("SELECT * FROM coords_of_jobs", conn)

    my_map = go.Figure(data=go.Scattergeo(
        lat=coords_df['latitude'],
        lon=coords_df['longitude'],
        text=git_df['text'],
        mode='markers'
    ))

    my_map.update_layout(
        title='Github Jobs in the USA',
        geo_scope='usa',
    )
    my_map.show()


# gets all data into the database
def data_runner():
    my_git_data = get_git_jobs_data()
    my_so_data = get_stack_overflow_jobs_data()
    conn, cursor = open_database("my_db4.sqlite")
    setup_database(cursor)
    save_git_to_database(cursor, my_git_data)
    save_so_to_database(cursor, my_so_data)
    close_database(conn)


def main():
    my_git_data = get_git_jobs_data()
    # my_so_data = get_stack_overflow_jobs_data()
    data_runner()
    conn, cursor = open_database("my_db4.sqlite")
    create_coords_table(cursor)
    convert_location_to_coords_git(cursor, my_git_data)
    # convert_location_to_coords_so(cursor, my_so_data)
    close_database(conn)


if __name__ == '__main__':
    main()
    scatter_map()
