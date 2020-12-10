import socket
import json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from kafka import KafkaProducer, KafkaClient
import config
import time

producer = KafkaProducer(bootstrap_servers=['kafka:9092'])
#Stream Listener Class
class TweetsListener(StreamListener):

    # def __init__(self):
    #     # self.client_socket = csocket
    def on_data(self, data):
        try:
            producer.send(topic='Trump', value=data.encode('utf-8'))
            time.sleep(1000)
        except BaseException as e:
            print("Error %s" % str(e))
        return True


    def on_error(self, status):
        print(status)
        return True


# #Initializing the port and host
# host = 'localhost'
# port = 5599
# address = (host, port)

# #Initializing the socket
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind(address)
# server_socket.listen(5)

# print("Listening for client...")
# conn, address = server_socket.accept()

# print("Connected to Client at " + str(address))


# kafka = KafkaClient('localhost:9092')

trumpTweet = TweetsListener()


#authenticating
auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

#Establishing the twitter stream
twitter_stream = Stream(auth, trumpTweet, tweet_mode="extended_tweet")
twitter_stream.filter(track=['Trump'])