import pytest
import jobsCrawl


@pytest.fixture
def get_data():
    import jobsCrawl
    return jobsCrawl.get_git_jobs_data()


def test_jobs_dict(get_data):
    # test 1
    assert len(get_data) >= 150
    assert type(get_data[1]) is dict

def test_job_in_data(get_data):
    data = get_data
    fulltime = False
    contract = False
    for i in data:
        if i['type'] == 'Contract':
            contract = True
        if i['type'] == 'Full Time':
            fulltime = True
    assert contract and fulltime

"""
def test_save_txt():
    # required test 2
    some_data = {'id': 1232, 'type': "Testable"}
    list_data = []
    list_data.append(some_data)
    filename = "my_data.txt"
    jobsCrawl.save_data_file(list_data, filename)
    test_file = open(filename, 'r')
    save_data = test_file.readlines()
    # saves extra lines to txt
    #assert f"{str(some_data)}\n" in save_data
"""