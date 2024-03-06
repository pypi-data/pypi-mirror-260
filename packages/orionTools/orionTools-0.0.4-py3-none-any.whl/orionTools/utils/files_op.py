import json


def json_load(file_path):
    try:
        with open(file_path, encoding='utf-8') as json_file:
            file_data = json.load(json_file)
        return file_data
    except Exception as e:
        print(file_path, e)
        return {}
