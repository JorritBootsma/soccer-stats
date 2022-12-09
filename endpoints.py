from fastapi import Depends, FastAPI

import crud
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



# @app.post("/create_player", response_model=schemas.Player)
@app.post("/create_player")
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    # Possibly do some check here
    try:
        return crud.create_player(db=db, player=player)
    except IntegrityError as e:
        print('---')
        print(str(e))
        print('---')
        if "already exists." in str(e):
            return "ERROR: This player name already exists"
        else:
            raise BadRequest


# @app.post("/create_match")
# def create_match(db: Session = Depends(get_db)):
#     """
#     Create a match instance in the database.
#
#     :return:
#     """
#
#     match = schemas.MatchCreate()
#     res = crud.create_match(db)

