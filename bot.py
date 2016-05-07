from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API

from tweepy.streaming import StreamListener

consumer_key = "agjequxG75iT0dHxn7jCd1uLW"
consumer_secret = "HxwaAwLisDBiZqBTqLt4AVDHMcba0ZRRyJobwjZ2ubMdgRhVXo"
access_token_key = "2450454258-64KnS3q2NcT2Ti3gjQa8UDq0rMIXVRfnXQRWB4U"
access_token_secret = "KRG6K0y6KaJr56qqSADwSdmUSOuxbyUvKV8RRR8oQd9B5"

class Listener( StreamListener ):

    def __init__( self ):
        self.tweetCount = 0

    def on_connect( self ):
        print("Connection established!!")

    def on_disconnect( self, notice ):
        print("Connection lost!! : ", notice)

    def on_data( self, status ):
        print("Entered on_data()")
        print(status, flush = True)
        return True

    def on_direct_message( self, status ):
        print("Entered on_direct_message()")
        try:
            print(status, flush = True)
            return True
        except BaseException as e:
            print("Failed on_direct_message()", str(e))

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

