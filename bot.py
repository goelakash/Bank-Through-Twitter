from __future__ import print_function
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API

from tweepy.streaming import StreamListener
import json
import re

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


EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

class Listener( StreamListener ):

    def __init__( self ):
        self.mesgCount = 0
        self.conn = httplib.HTTPSConnection('bluebank.azure-api.net')


    def str_list_to_json( self, response):
        response = response.split("}")
        response = response[:-1]
        for i in range(len(response)):
            response[i] = response[i][1:]   #[{...}, {...}, {...}]
            response[i] = response[i]+'}'
        for i in range(len(response)):
            response[i] = json.loads(response[i])
            # print(response[i])
        return response


    def get_accounts(self, cust_id):
        conn = self.conn
        conn.request("GET", "/api/v0.6.3/customers/"+cust_id+"/accounts", "", headers)
        data = str_list_to_json(conn.getresponse().read())

        accounts = []
        for x in data:
            accounts.append(x)
        return accounts


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

            if text[0] == "help":
                # list all the commands


            '''
            1. Account info
            '''
            elif text[0] == "account" and text[1] == "info":
                try:
                    accounts = self.get_accounts(customer_id)
                    for k,acc in zip(range(len(data)),data):
                        print(k+1,".")
                        print("Acc no: ",acc["accountNumber"])
                        print("Acc type: ",acc["accountType"])
                        print("Acc balance: ",acc["accountBalance"] + " "+ acc["accountCurrency"])
                except e:
                    print("Exception: ",e)


            '''
            2. Transaction history
            '''
            elif text[0] == "transaction" and text[1] == "history":
                limit = 5
                try:
                    if text[2]:
                        if text[2].isdigit():
                            limit = int(text[2])
                        else:
                            raise ValueError('Illegal value!')

                    accounts = self.get_accounts(customer_id)
                    print("Description | Amount | DateTime | Balance")

                    for acc in accounts:
                        print("for account no: ",acc["accountNumber"],")")
                        self.conn.request("GET", "/api/v0.6.3/accounts/"+acc["accountNumber"]+"/transactions?limit="+limit,"",headers)
                        response = conn.getresponse()
                        data = str_list_to_json(response.read())

                        for i in range(len(data)):
                            print(i+1,". ",data[i]["transactionDescription"]," | ",data[i]["transactionAmount"]," | ",
                                data[i]["transactionDateTime"]," | ",data[i]["accountBalance"])


                except e:
                    print("An exception happened: ",e)

            '''
            3. User info
            '''
            elif text[0] == "my" and text[1]=="info":
                try:
                    if text[2] == "display":
                        self.conn.request("GET", "/api/v0.6.3/customers/"+customer_id,"",headers)
                        response = conn.getresponse()
                        data = json.loads(response().read())[0]
                        for x in data:
                            print(x+": "+data[x])

                    elif text[2] == "update":
                        if text[3] and text[4]:
                            if text[3] == "email":
                                if not EMAIL_REGEX.match(text[4]):
                                    raise ValueError('Invalid email address!')
                                body = {
                                    'emailID':text[4]
                                }
                                self.conn.request("PATCH","/api/v0.6.3/customers/"+customer_id,json.dumps(body), headers)

                            elif text[3] == "mobile":
                                if not text[4].isdigit() or not len(text[4])==10:
                                    raise ValueError('Invalid mobile number!')
                                body = {
                                    'mobilePhone':text[4]
                                }
                                self.conn.request("PATCH","/api/v0.6.3/customers/"+customer_id,json.dumps(body), headers)

                            else:
                                raise ValueError('Invalid arguments')

                        else:
                            raise IOError('Invalid arguments for update!')

                except e:
                    print("Exception occured: ",e)


            '''
            4. Payment (to account)
            '''
            elif text[0] == "pay" and text[1] and text[2]:
                try:
                    if len(text[1])==7 and text[1].isdigit():
                        try:
                            amount = float(text[2])
                        except ValueError:
                            "Not a float"

                        accounts = self.get_accounts(customer_id)

                        body = {
                          "toAccountNumber":text[1],
                          "toSortCode":"839999",
                          "paymentReference":"string",
                          "paymentAmount": amount
                        }
                        flag = 0
                        for acc in accounts:
                            conn.request("POST", "/api/v0.6.3/accounts/"+acc["id"]+"/payments", json.dumps(body), headers)
                            response = conn.getresponse

                            if str(response.status) == "200":
                                flag = 1
                                break
                        if flag==0:
                            raise SystemError('Cannot complete transaction!')
                except e:
                    print("Exception occured: ",e)
                #all atms

            '''
            5. Branches nearby
            '''
            elif text[0] == "branch" and text[1]=="near":
                # ask for lat and long or extract location from twitter

            '''
            6. ATMs nearby
            '''
            elif text[0] == "atm" and text[1]=="near":


            '''
            Invalid
            '''
            else:
                print("Unknown commands, please try again.")

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

