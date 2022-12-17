from typing import List

from sqlalchemy.orm import Session

import models
import schemas


def get_all_players(db: Session, skip: int = 0, limit: int = 10000):
    x = db.query(models.Player).offset(skip).limit(limit).all()
    print("---------------------------------------------")
    print(x)
    print("------------")
    print(x[0].birth_date)
    print(type(x[0].birth_date))
    print("---------------------------------------------")

    return x


def get_all_players_with_performance(db: Session, skip: int = 0, limit: int = 10000):
    x = db.query(models.Player).offset(skip).limit(limit).all()
    print("---------------------------------------------")
    print(x)
    print("------------")
    print(x[0].birth_date)
    print(type(x[0].birth_date))
    print("---------------------------------------------")

    return x


def get_all_teams(db: Session, skip: int = 0, limit: int = 10000):
    x = db.query(models.Team).offset(skip).limit(limit).all()
    print("---------------------------------------------")
    print(x)
    print("------------")
    print(x[0].club)
    print(type(x[0].club))
    print(x[0].id)
    print("---------------------------------------------")

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


# This operation needs more sophisticated logic to also possibly create goal= and card-
# entries. Probably using the .append method of SQLAlchemy
def create_match(db: Session, match_w_details: schemas.MatchCreate):
    match = {
        "date": match_w_details.date,
        "season": match_w_details.season,
        "their_goals": match_w_details.their_goals,
    }

    print(match)
    # print(match["home_team"])
    # print(type(match["home_team"]))

    db_match = models.Match(**match)

    db_home_team = models.Team(**match_w_details.home_team.dict())
    db_away_team = models.Team(**match_w_details.away_team.dict())
    print("######")
    print(db_home_team)
    print("######")
    print(db_match)
    db_match.home_team = db_home_team
    db_match.away_team = db_away_team

    # Add each present player to the match database object in players_present
    for player in match_w_details.players_present:
        db_player = models.Player(**player.dict())
        db_match.players_present.append(db_player)

    # Add each goal to the match database object in our_goals
    for goal in match_w_details.our_goals:
        # Convert goal_scorer and assist_giver back to Player database objects
        goal.goal_scorer = models.Player(**goal.goal_scorer.dict())
        if goal.assist_giver.name:
            goal.assist_giver = models.Player(**goal.assist_giver.dict())
        else:
            goal.assist_giver = None

        db_goal = models.Goal(**goal.dict())
        print("######")
        print(db_goal)
        print("######")
        db_match.our_goals.append(db_goal)

    for card in match_w_details.cards:
        # Convert card_receiver back to a Player database object
        if card.card_receiver.name:
            card.card_receiver = models.Player(**card.card_receiver.dict())
        else:
            card.card_receiver = None

        db_card = models.Card(**card.dict())
        db_match.cards.append(db_card)

    db.add(db_match)
    print("1###########################################################################")
    print(db_match)
    print("###########################################################################")
    db.commit()
    print("2###########################################################################")
    print(db_match.our_goals)
    print("###########################################################################")
    db.refresh(db_match)
    return db_match


def create_team(db: Session, team: schemas.TeamCreate):
    db_team = models.Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team