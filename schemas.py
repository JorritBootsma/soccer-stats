# Schemas defined in this module are Pydantic Models. FastAPI depends on these pydantic
# models for API interface definition. In this application we refer to the Pydantic
# Models as schemas to prevent confusion with the SQLAlchemy Models (defined in
# models.py). For clarity: these schemas define the expected input of the different
# endpoints, such as /create_match

import datetime
from typing import List, Optional

from pydantic import BaseModel


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
    name: Optional[str]
    birth_date: Optional[datetime.date]


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: Optional[int]

    class Config:
        orm_mode = True


class CardBase(BaseModel):
    card_type: str
    card_receiver: Player


class CardCreate(CardBase):
    pass


class Card(CardBase):
    id: int
    card_receiver_id: int
    match_id: Optional[int]

    class Config:
        orm_mode = True


class GoalBase(BaseModel):
    goal_scorer: Player
    assist_giver: Optional[Player]
    body_part: Optional[str]
    half: Optional[str]
    penalty_kick: Optional[bool]


class GoalCreate(GoalBase):
    pass


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
    players_present: List[Player] = []


class MatchCreate(MatchBase):
    our_goals: List[GoalCreate] = []
    cards: List[CardCreate] = []


class Match(MatchBase):
    id: int

    class Config:
        orm_mode = True


class MatchWithDetails(MatchBase):
    pass


class PlayerWithPerformance(PlayerBase):
    id: int
    goals_scored: List[Goal]
    assists_given: List[Goal]
    cards_received: List[Card]
    matches_played: List[Match]

    class Config:
        orm_mode = True
