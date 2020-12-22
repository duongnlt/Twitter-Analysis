const TwitterStreamChannels = require('twitter-stream-channels');
const credentials = require('./config.json');
const kafka = require('kafka-node')
const Producer = kafka.Producer

const clientKafka = new kafka.KafkaClient({kafkaHost: 'kafka:9092'})
const producerTrump = new Producer(clientKafka)
const producerBiden = new Producer(clientKafka)


const rt = "RT @"



const client = new TwitterStreamChannels(credentials);
const channels = {
	"trump" : ['trump'],
	"biden" : ['biden']
};
const stream = client.streamChannels({track:channels, language: 'en', tweet_mode: "extended_tweet"});
// console.log(stream)

stream.on('channels/trump',function(tweet){

    if (tweet.text.indexOf(rt) === -1) {
        const sendTweet = {
            "time": tweet.created_at,
            "user_id": tweet.user.id,
            "text": tweet.text,
            "user_followers_count": tweet.user.followers_count,
            "place": tweet.place,
            "location": tweet.user.location,
            "retweet_count": tweet.retweet_count,
            "favorite_count": tweet.favorite_count

        }
        const payloads = [{topic:'Trump',messages: JSON.stringify(sendTweet)}]
        // console.log(typeof sendTweet)

        if (producerTrump.ready) {
            producerTrump.send(payloads, function (err, data) {
                if (err) {
                    console.log(err)
                }
                console.log(data);
            });
        }
    }
});


stream.on('channels/biden',function(tweet){

    if (tweet.text.indexOf(rt) === -1) {
        const sendTweet = {
            "time": tweet.created_at,
            "user_id": tweet.user.id,
            "text": tweet.text,
            "user_followers_count": tweet.user.followers_count,
            "place": tweet.place,
            "location": tweet.user.location,
            "retweet_count": tweet.retweet_count,
            "favorite_count": tweet.favorite_count

        }
        const payloads = [{topic:'Biden',messages: JSON.stringify(sendTweet)}]
        if (producerBiden.ready) {
            producerBiden.send(payloads, function (err, data) {
                console.log(data);
            });
        }
    }
});



//If you want, you can listen on all the channels and pickup the $channels added by the module
//It contains the channel and the keywords picked up in the tweet
//stream.on('channels',function(tweet){
//    console.log(tweet.$channels,tweet.text);//any tweet with any of the keywords above
//});

//If you're really picky, you can listen to only some keywords
//stream.on('keywords/javascript',function(tweet){
//    console.log(tweet.text);//any tweet with the keyword "javascript"
//});

