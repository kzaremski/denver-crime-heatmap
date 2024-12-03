'''
CS 3120 Machine Learning Term Project
Denver Crime Heatmap
Konstantin Zaremski
December 1, 2024
'''

from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from app.database import engine 

Base = declarative_base()

class CrimePrediction(Base):
    __tablename__ = 'crime_predictions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    day_of_year = Column(Integer, nullable=False)
    hour = Column(Integer, nullable=False)
    crime_type = Column(Integer, nullable=True)
    crime_count = Column(Float, nullable=True)

    __table_args__ = (
        UniqueConstraint('x', 'y', 'day_of_year', 'hour', name='uix_x_y_day_hour'),
    )

    def __repr__(self):
        return f"<CrimePrediction(id={self.id}, x={self.x}, y={self.y}, day_of_year={self.day_of_year}, hour={self.hour}, crime_type={self.crime_type}, crime_count={self.crime_count})>"

# Create tables
Base.metadata.create_all(engine)
