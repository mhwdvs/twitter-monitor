import sys
import tweepy
import requests
import dhooks
import re
from dhooks import Webhook, Embed
from unshortenit import UnshortenIt


def run(chosenhandle, url):

    #frontloading basic tasks to improve efficiency
    urlexpander = UnshortenIt()

    #print("Number of Arguments: " + str(len(sys.argv)) + " arguments")
    #print("Argument List: " + str(sys.argv))

    #import keys from file
    with open ("devkeys.txt", "rt") as getkeys: # open file devkeys.txt for reading text data
        keys = getkeys.read()         # read the entire file into a string variable
    
    #use to see the contents of the key file
    #print("Your Twitter API Developer Keys are:")
    #print(keys)

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
            print("New tweet from monitored handle:")
            print(status.text)
            ifvoid = 0
            #finds "RT" in first 2 characters of a tweet (retweet)
            if((str(status.text[:2]).find("RT")) != -1):
                print("This is a retweet, we'll ignore this!")
                ifvoid = 1

            #finds "https://" anywhere in the tweet"
            elif((str(status.text).find("https://")) != -1 and ifvoid == 0):
                print("This tweet is an image or link.")

                #sends tweet contents to discord
                hook = Webhook(url)
                embed = Embed(
                    description = "New link/image from " + handle + ":"
                    )

                embed.add_field(name="Tweet Contents", value=str(status.text))
                embed.set_footer(text="Twitter Monitor -- github.com/izedout/twitter-monitor")

                hook.send(embed=embed)

                print("Tweet Sent to Discord!")

                #finds and sends expanded url to discord
                foundurls = re.findall(r'(https?://\S+)', str(status.text))
                urlnumber = len(foundurls)
                print("Number of URLs in tweet: " + str(urlnumber))
                currenturl = 1
                while currenturl <= urlnumber:
                    uri = urlexpander.unshorten(foundurls[currenturl - 1])
                    
                    hook = Webhook(url)

                    embed.add_field(name="Expanded URL:", value=uri)
                    embed.set_footer(text="Twitter Monitor -- github.com/izedout/twitter-monitor")

                    hook.send(embed=embed)

                    currenturl = currenturl + 1
                    print("Expanded URL " + uri + " Sent To Discord!")
                try:
                    media = status.extended_entities.get('media', [])
                    #print(len(media))
                    i = 0
                    while (i < len(media)):

                        hook = Webhook(url)

                        media_files = (media[i]['media_url'])
                        embed.set_image(media_files)

                        hook.send(embed=embed)
                        i = i + 1
                except:
                    print("Wasnt an image")

                finally:
                    print("Finished sending any images in tweet")
            #finds "@" in the first character of a tweet (reply)
            elif((str(status.text[:1]).find("@")) == 0 and ifvoid == 0):
                print("This is likely a reply, will not send")

            else:
                print("This is a regualr tweet, will send!")

                hook = Webhook(url)
                embed = Embed(
                    description = "New tweet from " + handle + ":"
                    )

                embed.add_field(name="Tweet Contents", value=str(status.text))
                embed.set_footer(text="Twitter Monitor -- github.com/izedout/twitter-monitor")

                hook.send(embed=embed)

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

    print("Now monitoring @" + handle + " for new tweets!")

    try:
        myStream.filter(follow=[str(client_id)])
    except KeyboardInterrupt:
        #stops monitor
        print("Monitor Stopped Successfully!")
        print("To monitor again, please re-run the script :)")
        #closes script, without "raise" the script restarts from the start of the while loop
        #raise
        raise SystemExit