from __future__ import print_function
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
import httplib, urllib

from tweepy.streaming import StreamListener
import json
import re

consumer_key = "5g9PIp3wwXjVqgkYVFIVGyI2x"
consumer_secret = "X0BkFrvWoxz9lV1q9XTs7z2dBb0Lh5ZYnx4Zrzsq9ZiKAHzC6N"
access_token_key = "728681427718524929-duiQPYVfp6dQuG2UMpvVpkQH15kk7Sm"
access_token_secret = "8aYVeG2m18TRHdLHBSiJGlkJjiZ3rEzhgZQecZwffzbga"

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
        if not response:
            return []
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
        data = self.str_list_to_json(conn.getresponse().read())

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
            if mesg["sender"]["name"]=="Archie":
                return
            self.mesgCount += 1
            text = mesg["text"]
            print("\nNew message: ",self.mesgCount)
            print("\nSender Name: ",mesg["sender"]["name"])
            print("Sender screen name: ",mesg["sender_screen_name"])
            print("Text received: ",mesg["text"])
            print("Sent at: ",mesg["created_at"])
            # api.send_direct_message(screen_name=mesg["sender_screen_name"], text="Message received: "+text)

            text = text.lower().split(" ")
            print(text)

            if text[0] == "help":
                # list all the commands
                pass

                '''
                1. Account info
                '''
            elif len(text)>=2 and text[0] == "account" and text[1] == "info":
                try:
                    print("Getting account info-\n")
                    accounts = self.get_accounts(customer_id)
                    for k,acc in zip(range(len(accounts)),accounts):
                        print(k+1,".")
                        print("Acc no: ",acc["accountNumber"])
                        print("Acc type: ",acc["accountType"])
                        print("Acc balance: ",str(acc["accountBalance"]) + " " + acc["accountCurrency"])
                except Exception as e:
                    print("Exception: ",e)


                '''
                2. Transaction history
                '''
            elif len(text)>=2 and text[0] == "transaction" and text[1] == "history":
                limit = 3
                try:
                    if len(text)>=3 and text[2]>0:
                        if text[2].isdigit():
                            limit = int(text[2])
                        else:
                            raise ValueError('Illegal value!')

                    accounts = self.get_accounts(customer_id)
                    print("No. of accounts: ",len(accounts))
                    print("Description | Amount | DateTime | Balance")

                    for acc in accounts:
                        print("(for account no: ",acc["accountNumber"],")\n")

                        self.conn.request("GET", "/api/v0.6.3/accounts/"+str(acc["id"])+"/transactions?limit="+str(limit),"",headers)
                        # print("Query done\n")
                        response = self.conn.getresponse()
                        # print("Response received\n")
                        data = self.str_list_to_json( response.read() )
                        # print(data)
                        print("Length of data: ",len(data))
                        for i in range(len(data)):
                            print(i+1,". ",data[i]["transactionDescription"]," | ",data[i]["transactionAmount"]," | ",
                                data[i]["transactionDateTime"]," | ",data[i]["accountBalance"])


                except Exception as e:
                    print("An exception happened: ",e)

                '''
                3. User info
                '''
            elif len(text)>=2 and text[0] == "my" and text[1]=="info":
                try:
                    if len(text)>=3 and text[2] == "display":
                        self.conn.request("GET", "/api/v0.6.3/customers/"+str(customer_id),"",headers)
                        response = self.conn.getresponse()
                        data = json.loads(response.read())[0]
                        for x in data:
                            print(x+": "+data[x])

                    elif len(text)>=3 and text[2] == "update":
                        print("Update successful!\n")

                        if len(text)>=5:
                            if text[3] == "email":
                                if not EMAIL_REGEX.match(text[4]):
                                    raise ValueError('Invalid email address!')
                                body = {
                                    'emailID':text[4]
                                }
                                self.conn.request("PATCH","/api/v0.6.3/customers/"+str(customer_id),json.dumps(body), headers)
                                print(self.conn.getresponse().status)

                            elif text[3] == "mobile":
                                if not text[4].isdigit() or not len(text[4])==10:
                                    raise ValueError('Invalid mobile number!')
                                body = {
                                    'mobilePhone':str(text[4])
                                }
                                self.conn.request("PATCH","/api/v0.6.3/customers/"+customer_id,json.dumps(body), headers)

                            else:
                                raise ValueError('Invalid arguments')

                        else:
                            raise IOError('Invalid arguments for update!')
                    else:
                        raise IOError('Need more arguments!')

                except Exception as e:
                    print("Exception occured: ",e)


                '''
                4. Payment (to account)
                '''
            elif len(text)>=3 and text[0] == "pay":
                try:
                    if len(text[1])==7 and text[1].isdigit():
                        try:
                            amount = float(text[2])
                        except ValueError:
                            "Not a float"

                        accounts = self.get_accounts(customer_id)

                        tdict =  {
                          "toAccountNumber":"6000018",
                          "toSortCode":"839999",
                          "paymentReference":"string",
                          "paymentAmount": 10.0
                        }
                        # flag = 0

                        ## OTP space
                        # print(json.dumps(body))
                        # for acc in accounts:
                        self.conn.request("POST", "/api/v0.6.3/accounts/572dbcc9fd3e5d6025180a0f/payments", json.dumps(tdict), headers)
                        response = self.conn.getresponse()
                        print("Response received\n")
                        print(response.read())

                            # if str(response.status) == "200":
                            #     flag = 1
                            #     break
                        # if flag==0:
                        #     raise SystemError('Cannot complete transaction!')
                except Exception as e:
                    print("Exception occured: ",e)
                #all atms

                '''
                5. Branches nearby
                '''
            elif text[0] == "branch" and text[1]=="near":
                # ask for lat and long or extract location from twitter
                pass
                '''
                6. ATMs nearby
                '''
            elif text[0] == "atm" and text[1]=="near":
                pass

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

        global api
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

