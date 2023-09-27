from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from rokit_app.db.model import TestResults
import os
username = os.getlogin()
db_file_path = f"/home/{username}/sql_db.db"
DATABASE_URL = f"sqlite:///{db_file_path}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class TestResultsDB(Base):
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True, index=True)
    test_name = Column(String)
    trial_number = Column(Integer)
    robot_name = Column(String)
    tracking_object = Column(String)
    temperature = Column(Float)
    humidity = Column(Float)
    inclination = Column(Float)
    floor_type = Column(String)
    notes = Column(String)
    velocity = Column(Float)

# Create tables
Base.metadata.create_all(bind=engine)

def create_test_results(results: TestResults):
    db_results = TestResultsDB(**results.dict())
    db = SessionLocal()
    db.add(db_results)
    db.commit()
    db.refresh(db_results)
    db.close()
