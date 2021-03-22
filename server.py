import os
from flask_marshmallow import Marshmallow
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from schema import Base, Tweet
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)
ma = Marshmallow(app)
engine = create_engine('sqlite:///tweets.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


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


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def screen_name_lookup():
    screen_name = request.form['screen_name'].replace(" ", "_")
    return redirect(url_for('get_tweets_by_screen_name', screen_name=screen_name))


@app.route('/<screen_name>/', methods=['GET'])
def get_tweets_by_screen_name(screen_name):
    if screen_name == '*':
        all_tweets = session.query(Tweet)
        # return tweets_schema.jsonify(all_tweets)
        return render_template('success.html', json_data=all_tweets)
    else:
        user_tweets = session.query(Tweet).filter(func.lower(Tweet.screen_name) == screen_name.lower()).all()
        user_tweets_length = len(user_tweets)

        if user_tweets_length == 0:
            return render_template('oops.html')

        return render_template(
            'success.html',
            json_data=user_tweets
        )


app.run(host='0.0.0.0', port=os.environ.get('PORT'))
