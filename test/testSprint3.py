import pytest
import jobsDB


@pytest.fixture(scope="module")
def test_database():
    conn, cur = jobsDB.open_database("my_db4")
    return cur


def test_check_jobs(test_database):
    location = test_database.execute("""SELECT location from jobs_api_data where id=0e921dfd-4f8c-4a4d-8adb-f356859db1e7""")
    assert location == "Lake Forest, CA"
