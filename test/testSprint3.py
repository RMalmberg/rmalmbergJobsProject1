import pytest


@pytest.fixture
def get_data():
    import jobsCrawl
    return jobsCrawl.get_stackoverflow_jobs_data()
