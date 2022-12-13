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
def create_match(db: Session, match: schemas.MatchCreate):
    db_match = models.Match(**match.dict())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


def create_team(db: Session, team: schemas.TeamCreate):
    db_team = models.Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team