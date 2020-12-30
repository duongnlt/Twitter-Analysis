import matplotlib.pyplot as plt

# x = [50, 50]

# fig, axarr = plt.subplots(3)

# # draw the initial pie chart
# axarr[0].pie(x,autopct='%1.1f%%')

from kafka import KafkaConsumer
import time

consumer1 = KafkaConsumer('trump_visualize', bootstrap_servers=['localhost:19092'])
consumer2 = KafkaConsumer('biden_visualize', bootstrap_servers=['localhost:19092'])

for msg1, msg2 in zip(consumer1, consumer2):
    print(msg1.value)
    print(msg2.value)
    time.sleep(5)
