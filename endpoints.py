from fastapi import Depends, FastAPI

import crud
import initial_load
from models import *
import schemas
from database import Session, engine
from sqlalchemy.exc import IntegrityError

app = FastAPI(debug=True)


class BadRequest(Exception):
    pass


# Dependency
def get_db():
    Session.configure(autocommit=False, autoflush=False, bind=engine)
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Homepage"}


@app.delete("/initialize_tables")
def initialize_tables():
    initial_load.drop_and_create(Base, engine)
    initial_load.fill_players_table()
    initial_load.fill_teams_table()
    return True


@app.get("/get_all_players", response_model=list[schemas.Player])
def get_all_players(db: Session = Depends(get_db)):
    players = crud.get_all_players(db)
    print(players)
    return players


@app.get("/get_all_teams", response_model=list[schemas.Team])
def get_all_teams(db: Session = Depends(get_db)):
    teams = crud.get_all_teams(db)
    print(teams)
    return teams


# This is commented out for now due to varying return values-types, might include later
# @app.post("/create_player", response_model=schemas.PlayerCreate)
@app.post("/create_player")
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    # Possibly do some check here
    try:
        return crud.create_player(db=db, player=player)
    except IntegrityError as e:
        if "already exists." in str(e):
            return "ERROR: This player name already exists"
        else:
            print('---')
            print(str(e))
            print('---')
            raise BadRequest


@app.post("/create_team")
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    return crud.create_team(db=db, team=team)


@app.post("/create_goal")
def create_goal(goal: schemas.GoalCreate, db: Session = Depends(get_db)):
    return crud.create_goal(db=db, goal=goal)


# @app.post("/create_card")
# def create_card(card: schemas.CardCreate, db: Session = Depends(get_db)):
#     return crud.create_card(db=db, card=card)


# @app.post("/create_match")
# def create_match(match: schemas.MatchCreate, db: Session = Depends(get_db)):
#     """
#     Create a match instance in the database.
#
#     :return:
#     """
#
#     match = schemas.MatchCreate()
#     res = crud.create_match(db)
