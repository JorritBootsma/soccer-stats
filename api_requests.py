# This module contains functions that are called from the frontend and send a request to the backend.
import json

import requests

BASE_URL = "http://127.0.0.1:8000/"


def send_to_database(session_state):
    # requests.post()
    session_state["save_match_to_db"] = "TO BE IMPLEMENTED"


def create_player(name, birth_date):
    url_suffix = "create_player"
    full_url = BASE_URL + url_suffix
    player = {"name": name, "birth_date": birth_date}
    response = requests.post(full_url, json=player)
    return response


def create_team(team):
    url_suffix = "create_team"
    full_url = BASE_URL + url_suffix
    team = {"club": team}
    response = requests.post(full_url, json=team)
    return response


def initialize_tables():
    url_suffix = "initialize_tables"
    full_url = BASE_URL + url_suffix
    response = requests.delete(full_url)
