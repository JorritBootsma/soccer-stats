# Schemas defined in this module are Pydantic Models. FastAPI depends on these pydantic
# models for API interface definition. In this application we refer to the Pydantic
# Models as schemas to prevent confusion with the SQLAlchemy Models (defined in
# models.py)

import datetime
from typing import List, Optional

from pydantic import BaseModel


class CardBase(BaseModel):
    card_type: str
    match_id: int


class CardCreate(CardBase):
    pass


class Card(CardBase):
    id: int

    class Config:
        orm_mode = True


class GoalBase(BaseModel):
    goal_scorer: str
    assist_giver: Optional[str]
    body_part: Optional[str]
    half: Optional[str]


class GoalCreate(GoalBase):
    pass


class Goal(GoalBase):
    id: int

    class Config:
        orm_mode = True


class PlayerBase(BaseModel):
    name: str
    # birth_date: Optional[datetime.datetime]
    birth_date: str


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int

    class Config:
        orm_mode = True


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


class TeamBase(BaseModel):
    club: str

    class Config:
        orm_mode = True


class TeamCreate(TeamBase):
    pass
