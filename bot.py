import kanye
import time
import tweepy
import os
from queue import LifoQueue
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schema import Base, Tweet

# ///////////////////Database///////////////////
engine = create_engine('sqlite:///tweets.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


# /////////////////Twitter API/////////////////
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_KEY = os.environ['ACCESS_KEY']
ACCESS_SECRET = os.environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


# //////////////Tweet Response/////////////////
def reply_to_tweets(interval: int):
    session = DBSession()
    stack = LifoQueue(maxsize=0)

    print("Searching for new tweets...")

    mentions = api.mentions_timeline()

    last_replied_to_query = session.query(
        Tweet).order_by(Tweet.id.desc()).first()
    last_replied_id = None

    if last_replied_to_query is not None:
        last_replied_id = last_replied_to_query.tweet_id

    for mention in mentions:
        if mention.id_str != last_replied_id and '#kanye' in mention.text.lower():
            stack.put(mention)
        else:
            break

    while not stack.empty():
        mention = stack.get()
        print('Responding to, @{}: {}'.format(mention.user.screen_name, mention.text))

        kanye_reply = kanye.get_new_quote()
        new_tweet = Tweet(
            tweet_id=mention.id_str,
            screen_name=mention.user.screen_name,
            text=mention.text,
            response=kanye_reply
        )

        session.add(new_tweet)
        session.commit()
        api.update_status(
            '@{} {}'.format(mention.user.screen_name, kanye_reply), mention.id)

    print("Done responding, searching again in {} seconds...".format(interval))
    session.close()


# Bot Timer
if __name__ == "__main__":
    while True:
        t = 60 * 60
        reply_to_tweets(t)
        time.sleep(t)
