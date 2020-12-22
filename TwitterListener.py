import socket
import json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from kafka import KafkaProducer, KafkaClient
import config
import time
import tweepy
import csv
import logging
import ssl

from urllib3.exceptions import ReadTimeoutError
from requests.exceptions import Timeout, ConnectionError

logging.basicConfig(level=logging.INFO)



# producer = KafkaProducer(bootstrap_servers=['localhost:19092'])

def make_data(raw_data):
    send_data = {}
    if 'created_at' in raw_data:
        send_data['time'] = raw_data['created_at'] 
    else:
        send_data['time'] = None
    send_data['text'] = raw_data['text']
    if 'user' in raw_data:
        send_data['user_followers_count'] = raw_data['user']['followers_count']
        send_data['user_id'] = raw_data['user']['id']
    else:
        send_data['user_followers_count'] = None
        send_data['user_id'] = None
    # send_data['user_followers_count'] = raw_data['user']['followers_count']
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
        
        if 'text' not in data:
            return True
        send_data = json.loads(make_data(data))
        try:
            tweet_text = send_data['text']
            tweet_text = (tweet_text.replace('&amp;', '&').replace('&lt;', '<')\
                     .replace('&gt;', '>').replace('&quot;', '"')\
                     .replace('&#39;', "'").replace(';', " ")\
                     .replace(r'\u', " "))
            
            if not any((('RT @' in tweet_text, 'RT' in tweet_text, tweet_text.count('@') >= 2, tweet_text.count('#') >= 3))):
                # print(tweet_text)
                writer.writerow([send_data['time'], send_data['user_id'], tweet_text,
                                send_data['user_followers_count'], send_data['place'], send_data['location'], send_data['retweet_count'], send_data['favorite_count']])

        except BaseException as e:
            print("Error %s" % str(e))
            pass
        
        return True


    def on_error(self, status):
        print(status)
        return True






#authenticating
auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

def work():

    with open("trumptweets.csv", "a", encoding='utf-8') as f:
        global writer
        writer = csv.writer(f)

        # writer.writerow(["time", "user_id", "text", 'user_followers_count', 'place', 'location', 'retweet_count', 'favorite_count'])

        try:
            streamingAPI = tweepy.streaming.Stream(auth, TweetsListener(), tweet_mode="extended_tweet")
            streamingAPI.filter(track=['Trump'], languages=["en"])

        # Stop temporarily when hitting Twitter rate Limit
        except tweepy.RateLimitError:
            print("RateLimitError...waiting ~15 minutes to continue")
            time.sleep(1001)
            streamingAPI = tweepy.streaming.Stream(auth, TweetsListener(), tweet_mode="extended_tweet")
            streamingAPI.filter(track=['Trump'], languages=["en"])
        
        except (Timeout, ssl.SSLError, ReadTimeoutError, ConnectionError) as exc:
            print("Timeout/connection error...waiting ~15 minutes to continue")
            time.sleep(1001)
            streamingAPI = tweepy.streaming.Stream(auth, TweetsListener())
            streamingAPI.filter(track=['Trump'], languages=["en"], tweet_mode="extended_tweet")
        except tweepy.TweepError as e:
            if 'Failed to send request:' in e.reason:
                print("Time out error caught.")
                time.sleep(1001)
                streamingAPI = tweepy.streaming.Stream(auth, TweetsListener())
                streamingAPI.filter(track=['Trump'], languages=["en"], tweet_mode="extended_tweet")
            else:
                print("Other error with this user...passing")
                pass



if __name__ == '__main__':
    work()
