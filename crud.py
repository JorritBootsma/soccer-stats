from typing import List

from sqlalchemy.orm import Session

import models
import schemas


def get_player_by_id(db: Session, id):
    x = db.query(models.Player).filter(models.Player.id == id).one()
    return x


def get_team_by_id(db: Session, id):
    x = db.query(models.Team).filter(models.Team.id == id).one()
    return x


def get_all_players(db: Session, skip: int = 0, limit: int = 10000):
    x = db.query(models.Player).offset(skip).limit(limit).all()
    return x


def get_player_goals(db: Session, player_id):
    x = db.query(models.Player).filter(models.Player.id == player_id).one()
    return x.goals_scored


def get_player_with_performance(db: Session, player_id):
    x = db.query(models.Player).filter(models.Player.id == player_id).one()
    return x


def get_all_players_with_performance(db: Session, skip: int = 0, limit: int = 10000):
    x = db.query(models.Player).offset(skip).limit(limit).all()
    return x


def get_all_teams(db: Session, skip: int = 0, limit: int = 10000):
    x = db.query(models.Team).offset(skip).limit(limit).all()
    return x


def get_all_matches(db: Session, skip: int = 0, limit: int = 10000):
    return db.query(models.Match).offset(skip).limit(limit).all()


def get_all_goals(db: Session, skip: int = 0, limit: int = 10000):
    return db.query(models.Goal).offset(skip).limit(limit).all()


def get_goals_by_player(db: Session, name: str):
    return db.query(models.Goal).filter(models.Goal.goal_scorer == name).all()


def get_goals_by_assist_giver(db: Session, name: str):
    return db.query(models.Goal).filter(models.Goal.assist_giver == name).all()


def create_card(db: Session, card: schemas.CardCreate):
    db_card = models.Card(**card.dict())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


def create_player(db: Session, player: schemas.PlayerCreate):
    db_player = models.Player(**player.dict())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return player


def create_goal(db: Session, goal: schemas.GoalCreate):
    db_goal = models.Goal(**goal.dict())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal


def create_match(db: Session, match_w_details: schemas.MatchCreate):
    match = {
        "date": match_w_details.date,
        "season": match_w_details.season,
        "their_goals": match_w_details.their_goals,
    }

    # This match instance is new and needs to be created
    db_match = models.Match(**match)

    # Look up home_team and away_team in Teams table and add to match
    db_home_team = get_team_by_id(db, match_w_details.home_team.id)
    db_match.home_team = db_home_team
    db_away_team = get_team_by_id(db, match_w_details.away_team.id)
    db_match.away_team = db_away_team

    # Add each present player to the match database object in players_present
    for player in match_w_details.players_present:
        # Look up player in Player database
        db_player = get_player_by_id(db, player.id)
        db_match.players_present.append(db_player)

    # Add each goal to the match database object in our_goals
    for goal in match_w_details.our_goals:
        # Look-up goal_scorer and assist_giver in Player database
        goal.goal_scorer = get_player_by_id(db, goal.goal_scorer.id)
        if goal.assist_giver.name:
            goal.assist_giver = get_player_by_id(db, goal.assist_giver.id)
        else:
            goal.assist_giver = None

        # This goal instance is new and needs to be created
        db_goal = models.Goal(**goal.dict())
        db_match.our_goals.append(db_goal)

    for card in match_w_details.cards:
        # Convert card_receiver back to a Player database object
        if card.card_receiver.name:
            card.card_receiver = models.Player(**card.card_receiver.dict())
        else:
            card.card_receiver = None

        # This card instance is new and needs to be created
        db_card = models.Card(**card.dict())
        db_match.cards.append(db_card)

    db.add(db_match)
    db.commit()

    # Some code on retreiving data from database by Player and by Team
    print('-----')
    mitch = get_player_by_id(db, id=15)
    print("ID = ", mitch.id)
    print("Goals scored:")
    print(mitch.goals_scored)
    print("Assists given:")
    print(mitch.assists_given)
    print("Cards received:")
    print(mitch.cards_received)
    print("Matches played:")
    print(mitch.matches_played)
    print("Number of Matches played:", len(mitch.matches_played))
    print('-----')
    print("###########################################################################")

    arsenal = get_team_by_id(db, id=1)
    print("Club = ", arsenal.club)
    print("# of Matches as home team: ", len(arsenal.matches_appeared_as_home))
    print("Matches as away team: ", len(arsenal.matches_appeared_as_away))
    db.refresh(db_match)


    return db_match


def create_team(db: Session, team: schemas.TeamCreate):
    db_team = models.Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team