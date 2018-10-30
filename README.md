# tweeper-the-twitter-monitor
Monitors Twitter for new tweets with filter capabilities, lightning-fast using Tweepy's Stream API

How to get up and going:

 - Sign up for a twitter developer account and create a new app. You will need twitter developer keys in order for this script to function.
 - Replace all caps twitter key sections with their respective keys. Please do not remove any of the quotes surrounding them, that will break the script :)
 - Install all dependancies (either with pip or manually downloading and adding them to your repository).
 - Run main.py

To Be Added:
 - URL expander so if the tweets you are monitoring are time-sensitive you can bypass the t.co redirection, that sometimes adds a few seconds of delay.
  
 - Filter for "@" only within the first character of a tweet
 
 - Currently just sends the tweet to a discord webhook, but would like to automate an action within the script, such as automatically opening the link in a new browser window and even automating that's actions if you are expecting what site you will be visiting

Feel free to leave more feature suggestions as issues :)

WORKING ONLY IN PYTHON 3.6!!! If you do not use this version primarily create an env, google it, I cant remember how but I know its the way it should be done.

I am not responsible if this is in any way abusing the Twitter API and resulting in you getting your developer account closed. In its current state it does not collect data or abuse get requests, and the stream API is supported by them because it it less resource intensive, so I think they should be cool with it :) 

DONT COLLECT DATA WITHOUT TWITTER's EXPLICIT PERMISSION!!! Privacy breaches are not cool, and can lead to more limited API's in future :(
