import sys
import tweepy
import requests
import discord_hooks
from discord_hooks import Webhook

def run(chosenhandle, url):

    print("Number of Arguments: " + str(len(sys.argv)) + " arguments")
    print("Argument List: " + str(sys.argv))

    #import keys from file
    with open ("devkeys.txt", "rt") as getkeys: # open file lorem.txt for reading text data
        keys = getkeys.read()         # read the entire file into a string variable
    
    #use to see the contents of the key file
    #print("Your Twitter API Developer Keys are:")
    #print(keys)  		          # print contents

    keylist = keys.splitlines()

    #use to test that the line split is working correctly
    #print(keylist[0])

    #this is redundant but verbose, consider removing
    apikey = keylist[0]
    apisecret = keylist[1]
    accesskey = keylist[2]
    accesssecret = keylist[3]

    auth = tweepy.OAuthHandler(apikey, apisecret)
    auth.set_access_token(accesskey, accesssecret)

    print(str(auth))

    api = tweepy.API(auth)

    class MyStreamListener(tweepy.StreamListener):

        def on_status(self, status):
            print(status.text)
            ifvoid = 0
            #finds "RT" in first 2 characters of a tweet (retweet)
            if((str(status.text[:2]).find("RT")) != -1):
                print("I think this is a retweet, we'll ignore this!")
                ifvoid = 1

            #finds "https://" anywhere in the tweet"
            elif((str(status.text).find("https://")) != -1 and ifvoid == 0):
                print("This tweet is an image or link!")

                embed = Webhook(url)
                embed.set_desc("@everyone - NEW LINK/IMAGE FROM " + handle + ":")
                embed.add_field(name="Tweet Contents", value=str(status.text))
                embed.set_footer(text="Twitter Monitor by @__ized on twitter",ts=True)

                embed.post()

            #finds "@" in the first character of a tweet (reply)
            elif((str(status.text[:1]).find("@")) == 0 and ifvoid == 0):
                print("This is likely a reply or other tweet, we will send this to discord but without an @")
                print("Tell the shitty dev of this program to comment out this functionallity if you want tweets in different channels")

                embed = Webhook(url)
                embed.set_desc("New non-link/image reply from " + handle + ":")
                embed.add_field(name="Tweet Contents", value=str(status.text))
                embed.set_footer(text="Twitter Monitor by @__ized on twitter",ts=True)

                embed.post()


    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

    #TEST CODE FOR TWITTER API
    #public_tweets = api.home_timeline()
    #for tweet in public_tweets:
    #    print(tweet.text)

    handle = chosenhandle
    print("This threads handle is @" + chosenhandle)
    type(handle)
    user = api.get_user(screen_name = handle)
    client_id = user.id
    #defines cybers twitter id, could become a user prompt for an @ and then converted to desired twitter id

    print("Now monitoring @" + handle + " for new tweets! RELAXXX")

    try:
        myStream.filter(follow=[str(client_id)])
    except KeyboardInterrupt:
        #stops monitor
        print("Monitor Stopped Successfully!")
        print("To monitor again, please re-run the script :)")
        #closes script, without "raise" the script restarts from the start of the while loop
        #raise
        raise SystemExit