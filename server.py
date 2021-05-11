import os
import json
from flask_marshmallow import Marshmallow
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from schema import Base, Tweet
from flask import Flask, render_template, request, jsonify


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
    all_tweets = session.query(Tweet).all()
    session.close()
    result = tweets_schema.dump(all_tweets)
    
    return render_template("index.html", tweets=result, count=len(all_tweets))


@app.route('/', methods=['POST', 'GET'])
def screen_name_lookup():
    screen_name = request.form['screen_name'].replace(" ", "_")
    session = DBSession()

    user_tweets = session.query(Tweet).filter(
        func.lower(Tweet.screen_name) == screen_name.lower()).all()
    user_tweets_length = len(user_tweets)
    session.close()

    if user_tweets_length == 0:
        return jsonify(results=f'No data found for: {screen_name}')
    return tweets_schema.jsonify(user_tweets)


app.run(host='0.0.0.0', port=os.environ.get('PORT'))
