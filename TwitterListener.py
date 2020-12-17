import socket
import json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from kafka import KafkaProducer, KafkaClient
import config
import time

import logging
logging.basicConfig(level=logging.INFO)



producer = KafkaProducer(bootstrap_servers=['localhost:19092'])

def make_data(raw_data):
    send_data = {}
    send_data['user_id'] = raw_data['user']['id']
    send_data['text'] = raw_data['text']
    send_data['user_followers_count'] = raw_data['user']['followers_count']
    send_data['place'] = raw_data['place']
    send_data['location'] = raw_data['user']['location']
    send_data['retweet_count'] = raw_data['retweet_count']
    send_data['favorite_count'] = raw_data['favorite_count']
    return json.dumps(send_data)

#Stream Listener Class
class TweetsListener(StreamListener):

    # def __init__(self):
    #     # self.client_socket = csocket
    def on_data(self, data):
        data = json.loads(data)
        send_data = make_data(data)
        future = producer.send(topic='Trump',value=str(send_data).encode('utf-8'))
        try:

            record_metadata = future.get(timeout=10)
            

        except BaseException as e:
            print("Error %s" % str(e))

        time.sleep(10)
        return True


    def on_error(self, status):
        print(status)
        return True




trumpTweet = TweetsListener()


#authenticating
auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

#Establishing the twitter stream
twitter_stream = Stream(auth, trumpTweet, tweet_mode="extended_tweet")
twitter_stream.filter(track=['Trump'])

