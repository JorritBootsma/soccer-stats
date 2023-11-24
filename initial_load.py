from api_requests import create_player, create_team
from helper_funcs.sql_funcs import get_all_table_names
from helper_funcs.general_funcs import load_json_from_filepath
import models  # import models to make sure SQLAlchemy knows about all our tables


TEAMS_CONFIG_PATH = "configs/teams.json"
PLAYERS_CONFIG_PATH = "configs/players.json"
teams = load_json_from_filepath(TEAMS_CONFIG_PATH)["teams"]
players = load_json_from_filepath(PLAYERS_CONFIG_PATH)["players"]


def create(sa_base, engine):
    print(f"All tables, initially: {get_all_table_names(engine)}")
    print(f"Tables in SQLAlchemy metadata: {sa_base.metadata.tables.keys()}")
    sa_base.metadata.create_all(engine)
    print(f"All tables after creating: {get_all_table_names(engine)}")


def drop_and_create(sa_base, engine):
    print(f"All tables, initially: {get_all_table_names(engine)}")

    # Drop all tables if present
    print(f"Tables in SQLAlchemy metadata: {sa_base.metadata.tables.keys()}")
    sa_base.metadata.drop_all(bind=engine)
    print(f"All tables after dropping: {get_all_table_names(engine)}")

    # Create tables
    sa_base.metadata.create_all(engine)
    print(f"All tables after creating: {get_all_table_names(engine)}")


def fill_players_table(player_list: list[dict] = players):
    """
    Bulk load a team of players.

    :param player_list: List[dict]
      Expected is a list of dictionaries with keys `name`, `birth_date` and `team_id`.
    :return:
     None
    """

    for player in player_list:
        print(player)
        name = player["name"]
        birth_date = player["birth_date"]
        team_id = player["team_id"]
        create_player(name, birth_date, team_id)


def fill_teams_table(teams_list: list[str] = teams):
    """
    Bulk load a competition of teams.

    :param teams_list: List[dict]
      Expected is a list of dictionaries with keys `name` and `birth_date`.
    :return:
     None
    """

    for team in teams_list:
        create_team(team)


if __name__ == "__main__":
    from database import Base, engine

    drop_and_create(Base, engine)
    fill_teams_table()
    fill_players_table()
