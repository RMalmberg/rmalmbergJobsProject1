
def test_is_job_there():
    found = False
    with open('../my_data.txt') as datafile:
        data = datafile.readlines()
        for line in data:
            print(line)
            if "Wellcome Sanger Institute" in line:
                found = True
    assert  found == True