# Schemas defined in this module are Pydantic Models. FastAPI depends on these pydantic
# models for API interface definition. In this application we refer to the Pydantic
# Models as schemas to prevent confusion with the SQLAlchemy Models (defined in
# models.py). For clarity: these schemas define the expected input of the different
# endpoints, such as /create_match

import datetime
from typing import List, Optional

from pydantic import BaseModel


class CardBase(BaseModel):
    card_type: str
    card_receiver: str


class CardCreate(CardBase):
    match_id: Optional[int]


class Card(CardBase):
    id: int
    card_receiver_id: int

    class Config:
        orm_mode = True


class TeamBase(BaseModel):
    club: str

    class Config:
        orm_mode = True


class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    id: int

    class Config:
        orm_mode = True


class PlayerBase(BaseModel):
    name: str
    birth_date: datetime.date


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int

    class Config:
        orm_mode = True


class GoalBase(BaseModel):
    goal_scorer: Player
    assist_giver: Optional[Player]
    body_part: Optional[str]
    half: Optional[str]
    penalty_kick: Optional[bool]


class GoalCreate(GoalBase):
    match_id: Optional[int]


class Goal(GoalBase):
    id: int
    match_id: int

    class Config:
        orm_mode = True


class MatchBase(BaseModel):
    date: datetime.date
    season: str
    home_team: Team
    away_team: Team
    their_goals: int
    players_present: Optional[List[Player]]


class MatchCreate(MatchBase):
    pass


class Match(MatchBase):
    id: int
    our_goals: list[Goal]
    cards: list[Card]

    class Config:
        orm_mode = True


class PlayerWithPerformance(PlayerBase):
    id: int
    goals_scored: List[Goal]
    assists_given: List[Goal]
    cards_received: List[Card]
    # matches_played: List[Match]

    class Config:
        orm_mode = True
