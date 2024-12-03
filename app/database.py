'''
CS 3120 Machine Learning Term Project
Denver Crime Heatmap
Konstantin Zaremski
December 1, 2024
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///app.db', echo=False)

Session = sessionmaker(bind=engine)

def get_session():
    """Returns a new session instance."""
    return Session()
    