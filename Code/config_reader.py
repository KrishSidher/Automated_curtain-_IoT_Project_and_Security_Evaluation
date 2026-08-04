import json

def json_to_dict():
    with open('config.json', 'r') as file:
        data = json.load(file)
    return data