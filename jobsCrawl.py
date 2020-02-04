# create JSON file from http request
# Sprint 1
# By Raina Malmberg of 490-004

import requests
import json

url = "https://jobs.github.com/positions.json?utf8=%E2%9C%93&description=&location="


def main():
    r = requests.get(url)
    x = r.json()

    with open('my_data.txt', 'w', encoding='utf-8') as file:
        json.dump(x, file, ensure_ascii=False, indent=4)


def count_data(filename: str):
    my_json = open(filename, 'r', encoding='utf-8')
    all_data = my_json.readlines()
    num_jobs = len(all_data)/10
    f = int(num_jobs)
    print(f)


def is_job(jobtitle: str):
    j_json = open('my_data.txt', 'r', encoding='utf-8')
    all_lines = j_json.readlines()

    res = [i for i in all_lines if jobtitle in i]
    """ prints only relevant entry with jobtitle string
     https://www.geeksforgeeks.org/python-finding-strings-with-given-substring-in-list/
    """
    print(str(res))


main()
print("my_data.txt written to directory containing jobsCrawl\nContains json info")
print("Below is the number of job entries written to the text file  'my_data.txt'")
count_data('my_data.txt')
print("\n\n Next is a Site Reliability Engineer posting from the GitHub Jobs API:\n")
is_job("Site Reliability Engineer")
