import json
from requests import Response


def load_json_from_filepath(filepath):
    with open(filepath) as json_data:
        try:
            dictionary = json.load(json_data)
        except json.JSONDecodeError:
            print("\nThe file has an invalid JSON format!")
            raise
    return dictionary


def response_to_json(response: Response) -> dict:
    return response.json()