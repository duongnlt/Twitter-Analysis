import socket
import json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from kafka import KafkaProducer, KafkaClient
import config
import time

# import logging
# logging.basicConfig(level=logging.INFO)



producer = KafkaProducer(bootstrap_servers=['localhost:19092'])
#Stream Listener Class
class TweetsListener(StreamListener):

    # def __init__(self):
    #     # self.client_socket = csocket
    def on_data(self, data):
        data = json.loads(data)
        future = producer.send(topic='Trump',value=data['text'].encode('utf-8'))
        try:

            record_metadata = future.get(timeout=10)
            

        except BaseException as e:
            print("Error %s" % str(e))

        time.sleep(30)
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

