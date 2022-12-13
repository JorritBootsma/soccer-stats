# This module contains functions that are called from the frontend and send a request to the backend.
import json
from typing import List
import requests
from requests import Response

import schemas

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


def create_goal(
        goal_scorer,
        assist_giver=None,
        body_part=None,
        half=None,
        penalty_kick=None,
        match_id=None
):
    url_suffix = "create_goal"
    full_url = BASE_URL + url_suffix
    goal = {
        "goal_scorer": goal_scorer,
        "assist_giver": assist_giver,
        "body_part": body_part,
        "half": half,
        "penalty_kick": penalty_kick,
        "match_id": match_id
    }
    response = requests.post(full_url, json=goal)
    return response


# def create_card(card_type, card_receiver, match_id)

def initialize_tables():
    url_suffix = "initialize_tables"
    full_url = BASE_URL + url_suffix
    response = requests.delete(full_url)


def get_all_players() -> Response:
    url_suffix = "get_all_players"
    full_url = BASE_URL + url_suffix
    response = requests.get(full_url)
    return response


def get_all_teams() -> Response:
    url_suffix = "get_all_teams"
    full_url = BASE_URL + url_suffix
    response = requests.get(full_url)
    return response