import subprocess

yn = 0
usrsubmit = 0
while yn = 0
  handles = input("What is/are the desired twitter handle/s? (DO NOT include @, seperate multiple handles with a space)")
  type(handles)
  handles = handles.split(" ")
  print("Handles Submitted: " + handles)
  print("Is this correct? Press *y* to continue or *n* to try again!")
  type(usrsubmit)
  #checks are untested
  if usrsubmit = "y"
    yn = 1
  else yn = 0

  #this subprocess is untested
i = 0
  while i < len(handles):
  subprocess.call(["python main.py", "-" + "handles[i]"])
  i = i + 1

print("All processes started!")
