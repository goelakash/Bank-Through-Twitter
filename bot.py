from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API

from tweepy.streaming import StreamListener

consumer_key = "agjequxG75iT0dHxn7jCd1uLW"
consumer_secret = "HxwaAwLisDBiZqBTqLt4AVDHMcba0ZRRyJobwjZ2ubMdgRhVXo"
access_token_key = "2450454258-64KnS3q2NcT2Ti3gjQa8UDq0rMIXVRfnXQRWB4U"
access_token_secret = "KRG6K0y6KaJr56qqSADwSdmUSOuxbyUvKV8RRR8oQd9B5"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token_key, access_token_secret)

api = API(auth)

# If the authentication was successful, you should
# see the name of the account print out
print("List of all received messages:\n\n")
print("receiver name: ",api.me().name)
print("receiver handle: ",api.me().screen_name)

messages = api.direct_messages()

for i in range(len(messages)):
    print("\n\nMessage: ",i)
    print("text: ",messages[i].text)
    print("sender name: ",messages[i].sender.name)
    print("sender hande: ",messages[i].sender_screen_name)
    # print("receiver handle: ",messages[i].recipient_screen_name)
    print("sent at: ",messages[i].created_at.strftime("%d-%m-%Y"))

