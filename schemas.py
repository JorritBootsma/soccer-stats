import datetime
from typing import List, Optional

from pydantic import BaseModel


class Card(BaseModel):
    id: int
    match_id: int
    card_type: str


class Goal(BaseModel):
    goal_scorer: str
    assist_giver: Optional[str]
    body_part: Optional[str]
    half: Optional[str]


class GoalCreate(Goal):
    pass


class Player(BaseModel):
    id: int
    name: str
    birth_date: datetime.datetime


class MatchBase(BaseModel):
    date: datetime.datetime
    season: str
    home_team: str
    away_team: str
    their_goals: int



class MatchCreate(MatchBase):
    pass


class Match(MatchBase):
    id: int

    class Config:
        orm_mode = True
