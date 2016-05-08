from __future__ import print_function
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
from google import search
from bs4 import BeautifulSoup
import httplib, urllib

from tweepy.streaming import StreamListener
import json
import re
import geocoder
from twilio.rest import TwilioRestClient

# Find these values at https://twilio.com/user/account
account_sid = "ACf9897f2a14fb2bf557b90131c4b328d2"
auth_token = "4e4f68aa42f26ed9f671548d9a30d620"
client = TwilioRestClient(account_sid, auth_token)

#twitter tokens
consumer_key = "5g9PIp3wwXjVqgkYVFIVGyI2x"
consumer_secret = "X0BkFrvWoxz9lV1q9XTs7z2dBb0Lh5ZYnx4Zrzsq9ZiKAHzC6N"
access_token_key = "728681427718524929-duiQPYVfp6dQuG2UMpvVpkQH15kk7Sm"
access_token_secret = "8aYVeG2m18TRHdLHBSiJGlkJjiZ3rEzhgZQecZwffzbga"

headers = {
    # Request headers
    'Content-Type':'application/json',
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
        self.payment_body = {}
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

            output="=====================\n"

            if text[0] == "help":
                # list all the commands
                output = "LIST of commands:\n\n"

                COMMANDS = {

                    "account info" : "Details of your Bank Accounts(Acc no., Acc. type and Acc. balance).",
                    "pay <Acc_no> <Amount>":"Pay to account number <Acc_no> amount equal to <Amount> GBP.",
                    "transaction history":"Last 3 transactions for each of your account.",
                    "transaction history <number>" : "Last <number> transactions for each of your account.",
                    "my info display":"Your registered personal info (Name, Address, Customer ID).",
                    # "branches near <address>":"List of all RBS branches nearby the address <address>.",
                    # "atms near <address>":"List of all ATMs nearby the address <address>."

                }
                count =0
                for k in COMMANDS.keys():
                    count += 1
                    output += str(count)+". "+k+": "+COMMANDS[k]+"\n\n"
                print(output)

            #OTP
            elif len(text)>=2 and len(text[0])==4 and text[0].isdigit() and len(text[1])==6 and text[1].isdigit():
                try:
                    if text[0]=="1234" and text[1]=="123456":
                        print("Valid credentials")
                        print(self.payment_body)

                        conn = httplib.HTTPSConnection('bluebank.azure-api.net')
                        conn.request("POST", "/api/v0.6.3/accounts/572dbcc9fd3e5d6025180a0f/payments", json.dumps(self.payment_body), headers)
                        response = conn.getresponse()
                        print("Response received\n")
                        data = self.str_list_to_json("["+response.read()+"]")
                        print(data)
                        output += "Payment info:"+"\n"
                        # print(response.read())
                        output += "To account: "+data[0]["toAccountNumber"]+"\n"
                        output += "Amount: "+data[0]["paymentAmount"]+"\n"
                        output += "Payment id: "+data[0]["id"]+"\n"
                    else:
                        raise IOError('Invalid credentials')

                except Exception as e:
                    print("Exception occured: ",e)

                '''
                1. Account info
                '''
            elif len(text)>=2 and text[0] == "account" and text[1] == "info":
                try:
                    print("Getting account info-\n")
                    accounts = self.get_accounts(customer_id)
                    for k,acc in zip(range(len(accounts)),accounts):
                        output += str(k+1)+"."+"\n"
                        output += "Acc no: "+acc["accountNumber"]+"\n"
                        output += "Acc type: "+acc["accountType"]+"\n"
                        output += "Acc balance: "+str(acc["accountBalance"]) + " " + acc["accountCurrency"]+"\n"
                except Exception as e:
                    print("Exception: ",e)


                '''
                2. Transaction history
                '''
            elif len(text)>=2 and text[0] == "transaction" and text[1] == "history":
                limit = "3"
                try:
                    if len(text)>=3 and int(text[2])>0:
                        if text[2].isdigit():
                            limit = text[2]
                        else:
                            raise ValueError('Illegal value!')

                    accounts = self.get_accounts(customer_id)
                    output += "No. of accounts: "+str(len(accounts))+"\n"
                    output += "Description | Amount | DateTime | Balance"+"\n"

                    for acc in accounts:
                        output += "(for account no: "+str(acc["accountNumber"])+")\n"+"\n"

                        self.conn.request("GET", "/api/v0.6.3/accounts/"+str(acc["id"])+"/transactions?limit="+str(limit),"",headers)
                        # print("Query done\n")
                        response = self.conn.getresponse()
                        # print("Response received\n")
                        data = self.str_list_to_json( response.read() )
                        for i in range(len(data)):
                            output += str(i+1)+". "+str(data[i]["transactionDescription"])+" | "+str(data[i]["transactionAmount"])+" | "
                            output += str(data[i]["transactionDateTime"])+" | "+str(data[i]["accountBalance"])+"\n"

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
                            output += (x+": "+data[x])+"\n"

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
                            print("Not a valid amount")

                        self.payment_body =  {
                          "toAccountNumber":"6000018",
                          "toSortCode":"839999",
                          "paymentReference":"string",
                          "paymentAmount": text[2]
                        }
                        print("Sending message")
                        message = client.messages.create(to="+919873000273", from_="+12052104853",
                                     body="123456")
                        print("Message sent")
                        output += "Enter PIN<space>OTP"

                except Exception as e:
                    print("Exception occured: ",e)


                '''
                5. Branches nearby
                '''
            elif len(text)>=3 and text[0] == "branches" and text[1]=="near":
                try:
                    print((" ").join(text[2:]))
                    g = geocoder.google((" ").join(text[2:]))
                    lat, lng = g.latlng
                    params = urllib.urlencode({
                    'lat':lat,
                    'lng':lng,
                    'radius':"10000"
                    })
                    #conn = httplib.HTTPSConnection('bluebank.azure-api.net')
                    print("Sending request")
                    self.conn.request("GET", "/api/v0.6.3/branches/near?%s" % params,"",headers)
                    print("Receiving response")
                    response = self.conn.getresponse()
                    # print(response.read())
                    data = self.str_list_to_json(response.read())

                    output = "List of nearby branches: "
                    for i in range(len(data)):
                        output += data[i]['branchName']+"+ "+data[i]['streetAddress']+", "+data[i]['city']+"\n"
                    # data = json.loads(response.read())
                    # for i in range(len(data)):
                    #     print(i+"1. ",data[i].branchName+", "+data[i].streetAddress+", "+data[i].city)

                except Exception as     e:
                    print("Exception occured:  ",e)

                # ask for lat and long or extract location from twitter
                pass
                '''
                6. ATMs nearby
                '''
            elif text[0] == "atms" and text[1]=="near":
                try:
                    g = geocoder.google((" ").join(text[2:]))
                    lat, lng = g.latlng
                    params = urllib.urlencode({
                    'lat':lat,
                    'lng':lng,
                    'radius':"10000"
                    })
                    #conn = httplib.HTTPSConnection('bluebank.azure-api.net')
                    self.conn.request("GET", "/api/v0.6.3/atms/near?%s" % params,"",headers)
                    response = self.conn.getresponse()
                    # print(response.read())
                    data = self.str_list_to_json(response.read())

                    output = "List of nearby ATMs: "
                    for i in range(len(data)):
                        output += data[i]['atmName']+", "+data[i]['streetAddress']+", "+data[i]['city']+"\n"

                except Exception as e:
                    print("Exception occured:  ",e)

                '''
            #     7. faq

            #     '''
            elif len(text)>=2 and text[0] == "faq":
                    x=[]
                    for a in search(text[1], stop=10):
                        x.append(a)
                    #print(x)
                        r = urllib.urlopen(a)
                        soup = BeautifulSoup(r,"lxml")
                        data = soup.getText()
                        output += (' '.join(data[0:200].split()))
                        output += (a+"\n")

            else:
                output = ("Unknown commands. please try again.")

            api.send_direct_message(screen_name=mesg["sender_screen_name"], text=output)

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

