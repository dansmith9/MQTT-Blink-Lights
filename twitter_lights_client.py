import paho.mqtt.client as mqtt
from blinkt import set_pixel, show, clear
import time
from random import randint

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/oav/lights/221")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global NODE,r,g,b,current_pattern,PATTERNS

    values=str(msg.payload.decode('UTF-8')).split()
    if values[4]==node:
        r=0
        g=0
        b=0
        current_pattern="none"
        #time.sleep(10)
        clear()
        #print(msg.topic+" "+str(msg.payload.decode('UTF-8')))
        #print(values)
        try:
            r = int(values[0])
            g = int(values[1])
            b = int(values[2])
            print(r,g,b)
        except:
            print("Error")
            return
        current_pattern=values[3].lower()
        print("Pattern:",current_pattern)

## Sleep to allow time for network connectivity
#time.sleep(30)

# Constant to identify node
NODE="2"

## Set up variables for initial Blinkt display
current_pattern="solid"

r=109
g=101
b=158

## Set up MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#client.connect("192.168.1.100", 1883, 60)

#client.loop_start()

#Variable & loop to stop strange flickering on autorun...
last_pattern=""
while True:
    #print("Current pattern:",current_pattern)
    #print("Last pattern:",last_pattern)
    if last_pattern!=current_pattern:
        print("Inside loop check")
        if r!=0 or g!=0 or b!=0:
            if current_pattern=="fade":
                #print("Fade")
                i = 0.0
                while i<=1:
                    for j in range(0,8):
                        set_pixel(j,r,g,b,i)
                    show()
                    i+=0.01
                i-=0.1
                time.sleep(1)
                while i>=0:
                    for j in range(0,8):
                        set_pixel(j,r,g,b,i)
                    show()
                    i-=0.01
                time.sleep(1)
                for j in range(0,8):
                    set_pixel(j,0,0,0,1)
            elif current_pattern=="dot":
                #print("dot")
                for i in range(8):
                    clear()
                    #print(i)
                    set_pixel(i,r,g,b)
                    show()
                    time.sleep(0.5)
                for i in range(6,0,-1):
                    clear()
                    #print(i)
                    set_pixel(i,r,g,b)
                    show()
                    time.sleep(0.5)
            elif current_pattern=="random":
                #print("random")
                clear()
                random_pixel=randint(0,7)
                #print(random_pixel)
                set_pixel(random_pixel,r,g,b)
                show()
                time.sleep(0.5)
            elif current_pattern=="solid":
                #print("solid")
                for j in range(0,8):
                    set_pixel(j,r,g,b)
                show()

        last_pattern=current_pattern
