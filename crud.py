from sqlalchemy.orm import Session

import models
import schemas


def get_all_matches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Match).offset(skip).limit(limit).all()


def get_all_goals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Goal).offset(skip).limit(limit).all()


def get_goals_by_player(db: Session, name: str):
    return db.query(models.Goal).filter(models.Goal.goal_scorer == name).all()


def get_goals_by_assist_giver(db: Session, name: str):
    return db.query(models.Goal).filter(models.Goal.assist_giver == name).all()


def create_goal(db: Session, goal: schemas.GoalCreate, match_id: int):
    db_goal = models.Goal(**goal.dict(), match_id=match_id)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal


def create_match(db: Session, match: schemas.MatchCreate):
    db_match = models.Match(**match.dict())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match
