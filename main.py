import sys
import tweepy
import requests
import discord_hooks
from discord_hooks import Webhook

def run(chosenhandle, url):

    print("Number of Arguments: " + str(len(sys.argv)) + " arguments")
    print("Argument List: " + str(sys.argv))

    auth = tweepy.OAuthHandler("API KEY HERE", "API SECRET HERE")
    auth.set_access_token("ACCESS TOKEN HERE", "ACCESS TOKEN SECRET HERE")

    api = tweepy.API(auth)

    class MyStreamListener(tweepy.StreamListener):

        def on_status(self, status):
            print(status.text)
            ifvoid = 0
            if((str(status.text).find("RT")) != -1):
                print("I think this is a retweet, we'll ignore this!")
                ifvoid = 1

            elif((str(status.text).find("https://")) != -1 and ifvoid == 0):
                print("This tweet is an image or link!")

                embed = Webhook(url)
                embed.set_desc("@everyone - NEW LINK/IMAGE FROM " + handle + ":")
                embed.add_field(name="Tweet Contents", value=str(status.text))
                embed.set_footer(text="Twitter Monitor by @__ized on twitter",ts=True)

                embed.post()

            elif((str(status.text).find("@")) == 0 and ifvoid == 0):
                #this is bad, i should only look for @ in the first character
                print("This is likely a reply or other tweet, we will send this to discord but without an @")
                print("Tell the shitty dev of this program to comment out this functionallity if you want tweets in different channels")

                embed = Webhook(url)
                embed.set_desc("New non-link/image reply from " + handle + ":")
                embed.add_field(name="Tweet Contents", value=str(status.text))
                embed.set_footer(text="Twitter Monitor by @__ized on twitter",ts=True)


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