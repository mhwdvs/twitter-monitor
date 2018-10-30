import tweepy
import requests
import discord_hooks
from discord_hooks import Webhook

auth = tweepy.OAuthHandler("API KEY HERE", "API SECRET HERE")
auth.set_access_token("ACCESS TOKEN HERE", "ACCESS TOKEN SECRET HERE")

api = tweepy.API(auth)

url = 'DISCORD WEBHOOK URL HERE'

class MyStreamListener(tweepy.StreamListener):

   def on_status(self, status):
    print(status.text)
    ifvoid = 0
    
    #filters out retweets, if you want to include retweets comment this out
    if((str(status.text).find("RT")) != -1):
        print("I think this is a retweet, we'll ignore this!")
        ifvoid = 1

    #sends to discord webhook if there is a link or image in the tweet (this can only see t.co url currently), change find string to any keyword you would like to filter for)
    elif((str(status.text).find("https://")) != -1 and ifvoid == 0):
        print("This tweet is an image or link!")

        embed = Webhook(url)
        embed.set_desc("@everyone - NEW LINK/IMAGE FROM " + handle + ":")
        embed.add_field(name="Tweet Contents", value=str(status.text))
        embed.set_footer(text="Tweeper the Twitter Monitor by @__ized/izedout",ts=True)

        embed.post()

    #Sends to discord currently if there is an @ anywhere in the tweet, should be revised to just first character 0_o
    elif((str(status.text).find("@")) == 0 and ifvoid == 0):
        #this is bad, i should only look for @ in the first character, FIX ME!!!
        print("This is likely a reply to other tweet, we will send this to discord")
        print("Tell the shitty dev of this program to comment out this functionallity if you want tweets in different channels")

        embed = Webhook(url)
        embed.set_desc("New non-link/image reply from " + handle + ":")
        embed.add_field(name="Tweet Contents", value=str(status.text))
        embed.set_footer(text="Twitter Monitor by @__ized on twitter",ts=True)


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

#TEST CODE FOR TWITTER API, IF YOU ARE HAVING ISSUES TEST IF THIS IS WORKING FOR YOU
#public_tweets = api.home_timeline()
#for tweet in public_tweets:
#    print(tweet.text)

#prompts user for desired twitter handle to monitor
handle = input("What is the desired twitter handle? (DO NOT include @)")
type(handle)
user = api.get_user(screen_name = handle)
client_id = user.id
#converts @ handle to client id that tweepy understands

print("Now monitoring @" + handle + " for new tweets! tweeper blesses your command prompt with tweets shortly ;)")

try:
    myStream.filter(follow=[str(client_id)])
except KeyboardInterrupt:
    #stops monitor
    print("Monitor Stopped Successfully!")
    print("To monitor again, please re-run the script :)")
    #closes script, without "raise" the script restarts from the start of the while loop
    #raise
    raise SystemExit
