import pytest
import jobsDB


@pytest.fixture()
def my_database():
    conn, cur = jobsDB.open_database("rmalmbergJobsProject1\\my_db4.sqlite")
    conn.commit()
    yield cur


def test_check_jobs(my_database):
    location = my_database.execute("""SELECT location from jobs_api_data where id='0e921dfd-4f8c-4a4d-8adb-f356859db1e7'""")
    assert location == "Lake Forest, CA"
