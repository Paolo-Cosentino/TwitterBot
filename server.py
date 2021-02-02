import os
from flask import Flask
from flask_marshmallow import Marshmallow
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from schema import Base, Tweet

app = Flask(__name__)
ma = Marshmallow(app)
engine = create_engine('sqlite:///tweets.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


class TweetSchema(ma.Schema):
    class Meta:
        fields = ('id',
                  'tweet_id',
                  'screen_name',
                  'text',
                  'response'
                  )


tweet_schema = TweetSchema()
tweets_schema = TweetSchema(many=True)


@app.route('/', methods=['GET'])
def home():
    session = DBSession()
    all_tweets = session.query(Tweet)
    return tweets_schema.jsonify(all_tweets)


@app.route('/<screen_name>/', methods=['GET'])
def get_tweets_by_screen_name(screen_name):
    session = DBSession()
    user_tweets = session.query(Tweet) \
        .filter(func.lower(Tweet.screen_name) == screen_name.lower()).all()
    if len(user_tweets) == 0:
        return f'<h1>No tweets found screen name: {screen_name}'
    return tweets_schema.jsonify(user_tweets)


app.run(host='0.0.0.0', port=os.environ.get('PORT'))
