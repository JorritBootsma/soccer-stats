from fastapi import Depends, FastAPI

import crud
import models
import schemas
from database import Session, engine
app = FastAPI(debug=True)

# Dependency
def get_db():
    Session.configure(autocommit=False, autoflush=False, bind=engine)
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.post("/send_to_database")
def send_to_database():
    """
    Placeholder for the request that sends the match data to the database.

    :return:
    """
    return ""


@app.post("/create_match")
def create_match(db: Session = Depends(get_db)):
    """
    Create a match instance in the database.

    :return:
    """

    match = schemas.MatchCreate()
    res = crud.create_match(db)

