from __future__ import print_function
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API

from tweepy.streaming import StreamListener
import json

consumer_key = "agjequxG75iT0dHxn7jCd1uLW"
consumer_secret = "HxwaAwLisDBiZqBTqLt4AVDHMcba0ZRRyJobwjZ2ubMdgRhVXo"
access_token_key = "2450454258-64KnS3q2NcT2Ti3gjQa8UDq0rMIXVRfnXQRWB4U"
access_token_secret = "KRG6K0y6KaJr56qqSADwSdmUSOuxbyUvKV8RRR8oQd9B5"

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '91282cc98ef2479b90d4e83d3d808b79',
    'bearer':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdXN0b21lcklkIjoiNTcyZGJjYzlmZDNlNWQ2MDI1MTgwYTBlIiwicm9sZSI6InVzZXIiLCJwcmltYXJ5U3Vic2NyaWJlcktleSI6IjkxMjgyY2M5OGVmMjQ3OWI5MGQ0ZTgzZDNkODA4Yjc5IiwiaWF0IjoxNDYyNjIwMzA4fQ.BrM6NP7N3FFAIu3CKfBat-ZnS8Qvupz9Q8QWz7GBbuE'
}

customer_id = "572dbcc9fd3e5d6025180a0e"

acc_id = ['572dbccafd3e5d6025180a10', #0 balance
'572dbcc9fd3e5d6025180a0f'] #14389.1

handle_to_customerid= {

    '_goelakash' : "572dbcc9fd3e5d6025180a0e"
}

class Listener( StreamListener ):

    def __init__( self ):
        self.mesgCount = 0

    def on_status(self, status):
        print("Status text!!")
        print(status.text)

    def on_connect( self ):
        print("Connection established!!")

    def on_disconnect( self, notice ):
        print("Connection lost!! : ", notice)

    def on_data( self, status ):
        print("Entered on_data()")
        jstr = json.loads(status)
        if "friends" not in jstr:
            mesg = jstr["direct_message"]
            self.mesgCount += 1
            text = mesg["text"]
            print("\nNew message: ",self.mesgCount)
            # print("\nSender Name: ",mesg["sender"]["name"])
            print("Sender screen name: ",mesg["sender_screen_name"])
            print("Text received: ",mesg["text"])
            print("Sent at: ",mesg["created_at"])

            text = text.lower().split(" ")
            conn = httplib.HTTPSConnection('bluebank.azure-api.net')

            if text[0] == "help":
                # list all the commands


            elif text[0] == "accounts":
                try:
                    if text[1] == "info":
                        conn.request("GET", "/api/v0.6.3/accounts/572dbcc9fd3e5d6025180a0f","",headers)
                        response = conn.getresponse()
                        data = response.read()
                        print(data)

                    elif text[1] == "update":
                        body = {
                            text[2]:text[3]
                        }
                        if text[2]=="accountFriendlyName":
                            conn.request("PATCH", "/api/v0.6.3/accounts/572dbcc9fd3e5d6025180a0f",body,headers)
                            response = conn.getresponse()
                            data = response.read()
                            print(data)

                        else:
                            print("Cannot update this attribute.")

                    elif text[1] == "payments":
                        conn.request("GET", "/api/v0.6.3/accounts/572dbcc9fd3e5d6025180a0f/payments","",headers)
                        response = conn.getresponse()
                        data = response.read()
                        print(data)

                    elif text[1] == "transactions":
                        conn.request("GET", "/api/v0.6.3/accounts/572dbcc9fd3e5d6025180a0f/transactions","",headers)
                        response = conn.getresponse()
                        data = response.read()
                        print(data)

                    else:
                        print("Illegal operation!\n")

                except e:
                    print("An exception happened: ",e)

            elif text[0] == "customers":
                try:
                    if text[1] == "all":
                        conn.request("GET", "/api/v0.6.3/customers","",headers)
                        response = conn.getresponse()
                        data = response.read()
                        print(data)

                    elif text[1] == "info":
                        conn.request("GET", "/api/v0.6.3/customers/"+customer_id,"",headers)
                        response = conn.getresponse()
                        data = response.read()
                        print(data)

                    elif text[1] == "accounts":
                        conn.request("GET", "/api/v0.6.3/customers/"+customer_id+"/accounts","",headers)
                        response = conn.getresponse()
                        data = response.read()
                        print(data)

                    elif text[1]  == "update":
                        body = {
                            text[2]:text[3]
                        }
                        if text[2]=="mobilePhone":
                            conn.request("PATCH", "/api/v0.6.3/customers/"+customer_id,"",headers)
                            response = conn.getresponse()
                            data = response.read()
                            print(data)


            elif text[0] == "list":

                if text[1] == "all":
                #all atms

                if text[1] == "near":
                # ask for lat and long or extract location from twitter

            elif text[0] == "branches":
                if text[1] == "all":
                #all branches

                if text[1] == "near":
                # ask for lat and long or extract location from twitter





        return True

    def on_error( self, status ):
        print(status)



def main():

    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.secure = True
        auth.set_access_token(access_token_key, access_token_secret)

        api = API(auth)

        # If the authentication was successful, you should
        # see the name of the account print out
        print(api.me().name)

        stream = Stream(auth, Listener())

        stream.userstream()

    except BaseException as e:
        print("Error in main()", e)

if __name__ == '__main__':
    main()

