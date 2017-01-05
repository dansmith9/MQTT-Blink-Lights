import time

try:
    from tweepy import Stream, OAuthHandler
    from tweepy.streaming import StreamListener
    import paho.mqtt.publish as publish
    import paho.mqtt.client as mqtt
except ImportError:
    exit("This script requires the tweepy module\nInstall with: sudo pip install tweepy")


ckey = 'JUYlZGrJxnnlZkHBRzKv3UsmO' # Consumer key
csecret = 'BbJlcMyf8SbHAVxmp7zpQAxtbmy6rzAyY10ldzGTxnRYcMUbOd' # Consumer secret
atoken = '3412692009-9lDbJSxkjZ9HhvdBNw7UNoxaQkDXXCSBVoi8qXp' # Access token
asecret = '258kVpynTZwRyV1UJHHZPxWHmQKjLjd8L6MS50nmJn0Jm' # Access secret
next_node=2


class listener(StreamListener):
    
    
    def on_status(self, status):
        global next_node
        PATTERNS=("fade","dot","random","solid")
        
        #text="#oavcomplights 200 100 50"
        print(status.author.screen_name)
        text = status.text
        split_text=text.split()
        print(split_text)
        if len(split_text)==5:
            print("In if")
            try:
                r_int = int(split_text[2])
                g_int = int(split_text[3])
                b_int = int(split_text[4])
            except:
                print("Error: invalid values:",split_text)
                return

            print(r_int)
            print(g_int)
            print(b_int)
            if r_int >=0 and r_int <=255:
                if g_int >=0 and g_int <=255:
                    if b_int >=0 and b_int <=255:
                        if split_text[1] in PATTERNS:
                            #print("success")
                            message=str(r_int)+" "+str(g_int)+" "+str(b_int)+" "+split_text[1]+" "+str(next_node)
                            print("Message:",message)
                            publish.single("/oav/lights/221", message, hostname="10.60.100.80",protocol=mqtt.MQTTv31)
                            if next_node==3:
                                next_node=0
                            else:
                                next_node+=1
                            print("Next node:",next_node)
                            
        return True

    def on_error(self, status):
        print(status)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterstream = Stream(auth, listener())
twitterstream.filter(track=['#oavcomplights'])
