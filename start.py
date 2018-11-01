import subprocess

yn = 0
while yn == 0:
  handles = input("What is/are the desired twitter handle/s? (DO NOT include @, seperate multiple handles with a space)")
  type(handles)
  handles = handles.split(" ")
  print("Handles Submitted: " + str(handles))
  print("Is this correct? Press *y* to continue or *n* to try again!")
  usrsubmit = input()
  #checks are untested
  if usrsubmit == "y":
    yn = 1
  else:
    yn = 0
    print("Restarting...")

#this subprocess is untested
i = 0
while i < len(handles):
  subprocess.call(["python main.py", "-" + handles[i]], shell=True)
  i = i + 1

print("All processes started!")
