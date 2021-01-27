import os
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Tweet(Base):
    __tablename__ = 'TWEETS'
    id = Column(Integer, primary_key=True)
    tweet_id = Column(String(255), nullable=False)
    screen_name = Column(String(255), nullable=False)
    text = Column(String(255), nullable=False)
    response = Column(String(255), nullable=False)

    def __repr__(self):
        return f"Tweet(tweet_id={self.tweet_id}, user={self.screen_name}, body={self.text},response={self.response})"


engine = create_engine('sqlite:///tweets.db')
Base.metadata.create_all(engine)
