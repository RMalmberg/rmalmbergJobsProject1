import pytest


@pytest.fixture
def get_data():
    import jsonCrawler
    return jsonCrawler.get_stackoverflow_jobs_data()
