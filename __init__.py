from src import Bunn as B
import asyncio
import sys
import html.parser as htmlparser
parser = htmlparser.HTMLParser()

users = {}
keyPhrase = "???"
active = False

def init():  
  pass

async def on_message(msg):
    if (active and keyPhrase != "???" and msg.message.lower().find(keyPhrase.lower())):
        addToRaffle(msg)
        
async def addToRaffle(msg):
    global users
        
    username = msg.message.display_name
    numId = msg.message.user_id
        
    for folks in users:
        if (folks == msg.message.user_id):
            await B.send_message("Looks like you're already in the raffle, @{}!".format(username))
            break
    users[username] = numId
    await B.send_message("@{} successfully joined the raffle!".format(username))
        
      
      
async def on_command(msg):
    global users
    global active
    global keyPhrase
  
    print(msg.message)
    msg.message = parser.unescape(msg.message)
    print(msg.message)
    cmd = msg.message[1:].split(" ")
    print(cmd)
   
    

    if (cmd[0] == "gatcha"):
        try:
            if (len(cmd) == 1):              
                if (active and keyPhrase != "???"):
                    await B.send_message("Raffle currently running! The key phase is >>>>> {}".format(keyPhrase))
                elif (active and keyPhrase == "???"):
                    await B.send_message("Oops! There's a raffle open, but there's no key phrase set! Kindly ask your host to set one using the '{0}{1} phrase' command!".format(msg.message[0], cmd[0]))
                else:
                    await B.send_message("There are no raffles open at this time.")
                    
                    
            elif (len(cmd) > 1):
                if (cmd[1] == "open"):
                  if (active):
                      await B.send_message("There is already an ongoing raffle!")
                  elif (not active):
                      active = True
                      await B.send_message("Raffle is now open for entry!")
                      await asyncio.sleep(1)
                      print(keyPhrase)
                      if (keyPhrase == "???"):                        
                          await B.send_message("Remember to set the key phrase using the '{0}{1} phrase' command!".format(msg.message[0], cmd[0]))
                  else:
                      active = False
                      await B.send_message("Error in raffle state ({})! Closing raffle...".format(active))   
                      
                      
                elif (cmd[1] == "close"):
                  if (active):
                      active = False
                      keyPhrase = "???"
                      await B.send_message("The raffle is now closed!")
                  elif (not active):
                      await B.send_message("There are no open raffles to close!")
                  else:
                      await B.send_message("Error in raffle state ({})! Closing raffle...".format(active)) 

                      
                elif (cmd[1] == "phrase"):
                  if (len(cmd) > 2):   
                      extraCmd = cmd
                      extraCmd = " ".join(extraCmd)  
                        
                      if (extraCmd != "???"):
                          keyPhrase = extraCmd
                          await B.send_message("""The NEW KEY PHRASE to enter the raffle is now >>>>> {}""".format(extraCmd))
                      if (extraCmd == "???"):
                          await B.send_message("Sorry, the default value isn't a valid key phrase.")
                       
                  elif (len(cmd) == 2):
                      if (keyPhrase != "???"):
                          await B.send_message("The key phrase is currently:      {}.".format(keyPhrase))  
                      elif (keyPhrase == "???"):
                          await B.send_message("There is no key phrase at this time. Please set one using the '{0}{1} phrase' command!".format(msg.message[0], cmd[0]))                  
                      else:
                          print("Unexpected value for key phrase: {}".format(keyPhrase))
                                
                  else:
                      await B.send_message("Sorry, '{0}' is an invalid {1} command".format(cmd[1], cmd[0]))
        except:
            print("Error in tambola.")
            print(sys.exc_info())
            pass

  
'''             
"open":
"close":
"clear": 
"help":
"spin":
"redo":
"phrase":
"add":  
"remove":
"blacklist":  
'''