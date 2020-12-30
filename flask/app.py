from flask import Flask, render_template, Response
import random
import json
import time
from datetime import datetime
from kafka import KafkaConsumer

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/biden-data')
def biden_data():
    def generate_random_data():
        # while True:
        #     neg = random.random()*100
        #     pos = random.random()*100
        #     neu = random.random()*100
        #     json_data = json.dumps(
        #         {'negative': neg, 'neutral': neu, 'positive': pos, 'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) 
        #     yield f"data:{json_data}\n\n"
        #     time.sleep(1)
        consumer_biden = KafkaConsumer('biden_visualize', bootstrap_servers=['localhost:19092'])
        pos = neg = neu = 0
        for msg in consumer_biden:
            data = json.loads(msg.value)
            if data['sentiment'] == "Positive":
                pos += 1
            elif data['sentiment'] == "Neutral":
                neu += 1
            elif data['sentiment'] == "Negative":
                neg += 1
            json_data = json.dumps({'negative': neg, 'neutral': neu, 'positive': pos, 'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            yield f"data:{json_data}\n\n" 

    return Response(generate_random_data(), mimetype='text/event-stream')

@app.route('/trump-data')
def trump_data():
    def generate_random_data():
        pos = neg = neu = 0
        consumer_trump = KafkaConsumer('trump_visualize', bootstrap_servers=['localhost:19092'])
        while True:
            for msg in consumer_trump:
                data = json.loads(msg.value)
                if data['sentiment'] == "Positive":
                    pos += 1
                elif data['sentiment'] == "Neutral":
                    neu += 1
                elif data['sentiment'] == "Negative":
                    neg += 1
                json_data = json.dumps({'negative': neg, 'neutral': neu, 'positive': pos, 'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
                yield f"data:{json_data}\n\n" 

    return Response(generate_random_data(), mimetype='text/event-stream')

if __name__ == '__main__':
   app.run()