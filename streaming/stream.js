const TwitterStreamChannels = require('twitter-stream-channels');
const credentials = require('./config.json');
const kafka = require('kafka-node')
const Producer = kafka.Producer

const clientKafka = new kafka.KafkaClient({kafkaHost: 'kafka:9092'})
const producerTrump = new Producer(clientKafka)
const producerBiden = new Producer(clientKafka)


var offset = new Date().getTimezoneOffset();
function pad(number, length){
    var str = "" + number
    while (str.length < length) {
        str = '0'+str
    }
    return str
}
offset = ((offset<0? '+':'-')+ // Note the reversed sign!
          pad(parseInt(Math.abs(offset/60)), 2)+
          pad(Math.abs(offset%60), 2))
console.log(offset);



const client = new TwitterStreamChannels(credentials);
const channels = {
	"trump" : ['trump'],
	"biden" : ['biden']
};
const stream = client.streamChannels({track:channels, language: 'en', tweet_mode: "extended_tweet"});
// console.log(stream)

stream.on('channels/trump',function(tweet){

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
    const payloads = [{topic:'Trump',messages: sendTweet}]
    // console.log(sendTweet)

    if (producerTrump.ready) {
        producerTrump.send(payloads, function (err, data) {
            console.log(data);
        });
    }
});

stream.on('channels/biden',function(tweet){

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
    const payloads = [{topic:'Biden',messages: sendTweet}]
    if (producerBiden.ready) {
        producerBiden.send(payloads, function (err, data) {
            console.log(data);
        });
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

setTimeout(function(){
    // await producer.disconnect()
    stream.stop();//closes the stream connected to Twitter
	console.log('>stream closed after 100 seconds');
},100000);