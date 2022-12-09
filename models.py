
from database import Base
from sqlalchemy import ForeignKey, Column, Integer, String, Date, ARRAY
from sqlalchemy.orm import relationship


class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    season = Column(String)

    home_team = Column(Integer, ForeignKey("teams.id"))
    away_team = Column(Integer, ForeignKey("teams.id"))

    their_goals = Integer

    our_goals = relationship("Goal", back_populates="match")
    cards = relationship("Card", back_populates="match")

    players_present = ARRAY(String(ForeignKey("players.id")))

    def __repr__(self):
        return f"<User(name='{self.name}', age='{self.age}')"


class Goal(Base):
    __tablename__ = "goals"
    goal_id = Column(Integer, primary_key=True)

    match_id = Column(Integer, ForeignKey("matches.id"))
    match = relationship("Match", back_populates="our_goals")

    # Assume only one goal scorer per goal (one-to-one)
    goals_scorer_id = Column(Integer, ForeignKey("players.id"))
    # goal_scorer = relationship("Player", back_populates="goals_scored", uselist=False)

    # Assume only one assist giver per goal (one-to-one)
    assist_giver_id = Column(Integer, ForeignKey("players.id"))
    # assist_giver = relationship("Player", back_populates="assists_given", uselist=False)

    body_part = Column(String(50))
    half = Column(String(10))

    def __repr__(self):
        return f"<Goal(match_id='{self.match_id}', scorer='{self.goal_scorer}')>"


class Card(Base):
    __tablename__ = "cards"
    card_id = Column(Integer, primary_key=True)

    match_id = Column(Integer, ForeignKey("matches.id"))
    match = relationship("Match", back_populates="cards")

    # Assume only one card receiver per card
    card_receiver_id = Column(Integer, ForeignKey("players.id"))
    # card_receiver = relationship("Player", back_populates="cards_received", uselist=False)

    card_type = Column(String)


class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    birth_date = Column(Date)

    # One player can have many goals_scored, assists_given and cards_received
    # goals_scored = relationship("Goal", back_populates="goal_scorer")
    # assists_given = relationship("Assist", back_populates="assist_giver")
    # cards_received = relationship("Card", back_populates="card_receiver")


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True)
    club = Column(String)
    team_number = Column(String(50))
    club_team_concat = club.concat(team_number)

    relationship("Match")


if __name__ == "__main__":
    import os
    import sqlalchemy

    # Connect to local PostgreSQL database
    server = "localhost"
    database = os.environ["USER"]
    conn_string = f"postgresql://{server}/{database}"
    print(conn_string)

    engine = sqlalchemy.create_engine(conn_string)

    def get_all_table_names(eng):
        all_tables = eng.execute(
                 """
                 SELECT
                     table_schema || '.' || table_name
                 FROM
                     information_schema.tables
                 WHERE
                     table_type = 'BASE TABLE'
                 AND
                     table_schema NOT IN ('pg_catalog', 'information_schema');
                 """
                ).fetchall()
        table_names_ = [tables_info[0] for tables_info in all_tables]
        return table_names_


    print(f"All tables: {get_all_table_names(engine)}")

    # Dummy code to drop specific tables using SQL query as string
    table_names = list(get_all_table_names(engine))
    sql = f"""DROP TABLE IF EXISTS {table_names[0]}, {table_names[1]} cascade;"""
    result = engine.execute(sql)
    print(f"Tables still left: {get_all_table_names(engine)}")

    # Drop all tables if present
    print(f"Tables in SQLAlchemy metadata: {Base.metadata.tables.keys()}")
    Base.metadata.drop_all(bind=engine)

    print(get_all_table_names(engine))

    # Create tables
    Base.metadata.create_all(engine)

    print(get_all_table_names(engine))