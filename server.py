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
    # print(all_tweets)
    session.close()
    return render_template("index.html", tweets=str(all_tweets), count=len(all_tweets))


# @app.route('/', methods=['POST'])
# def screen_name_lookup():
#     screen_name = request.form['screen_name'].replace(" ", "_")
#     if request.form.get('display-json'):
#         return redirect(url_for('get_tweets_by_screen_name', layout='json', screen_name=screen_name))
#     return redirect(url_for('get_tweets_by_screen_name', layout='table', screen_name=screen_name))


# @app.route('/<layout>/<screen_name>/', methods=['GET'])
# def get_tweets_by_screen_name(layout, screen_name):
#     if screen_name == '*':  # All tweets
#         if layout == 'json':
#             all_tweets = session.query(Tweet)
#             return tweets_schema.jsonify(all_tweets)
#         else:  # Table view for all tweets
#             all_tweets = session.query(Tweet)
#             return render_template('success.html', json_data=all_tweets, sn='*')
#     else:  # Tweets searched by screen_name
#         if layout == 'json':
#             user_tweets = session.query(Tweet).filter(func.lower(Tweet.screen_name) == screen_name.lower()).all()
#             user_tweets_length = len(user_tweets)
#             if user_tweets_length == 0:
#                 return jsonify(results=f'No data found for: {screen_name}')
#             return tweets_schema.jsonify(user_tweets)
#         else:  # Table view for search by screen_name
#             user_tweets = session.query(Tweet).filter(func.lower(Tweet.screen_name) == screen_name.lower()).all()
#             user_tweets_length = len(user_tweets)

#             if user_tweets_length == 0:
#                 return render_template('oops.html')
#             return render_template(
#                 'success.html',
#                 json_data=user_tweets,
#                 sn=screen_name
            # )

app.run(host='0.0.0.0', port=os.environ.get('PORT'))
