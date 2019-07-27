import threading
from threading import Thread
import apimethod

yn = 0
while yn == 0:
  with open ("webhook.txt", "rt") as webhookopen: # open file devkeys.txt for reading text data
    webhookurl = webhookopen.read()         # read the entire file into a string variable
  handles = input("What is/are the desired twitter handle/s? (DO NOT include @, seperate multiple handles with a space)")
  type(handles)
  #creates array from the string inputted by the user
  #this allows each handle to be sent to a different thread
  handles = handles.split(" ")
  print("Handles Submitted: " + str(handles))
  print("Is this correct? Enter *y* to continue or anything else to try again!")
  usrsubmit = input()
  if usrsubmit == "y":
    yn = 1
  else:
    yn = 0
    print("Restarting...")

#TREADING IS WORKING!
i = 0
numthreads = str(len(handles))
print(numthreads + " processes starting!")

def worker():
    apimethod.run(chosenhandle = str(handles[i]), url = webhookurl)
    chosenhandle = str(handles[i])
    print("Monitoring @" + chosenhandle)

while i <= len(handles) - 1:
  t = Thread(target=worker)
  t.start()
  i = i + 1

print("All processes started!")
