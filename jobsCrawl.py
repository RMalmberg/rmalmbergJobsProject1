import requests, json



url = "https://jobs.github.com/positions.json?utf8=%E2%9C%93&description=&location="

def main():
    r = requests.get(url)
    x = r.json()

    with open('my_data.txt', 'w', encoding='utf-8') as file:
        json.dump(x, file, ensure_ascii=False, indent=4)


def parse_json():
    my_json = open('my_data.txt', 'r', encoding='utf-8')
    some_data = [line.split('id:') for line in my_json.readlines()]
    print(len(some_data))

main()
parse_json()
#print_som_data()

