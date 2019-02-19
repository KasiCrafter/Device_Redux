import sys
import asyncio
#from src import Bytes
#from src import chat_pb2
from src import Bunn as B
#from src import Consts as C
#from src.bunnbot import Client 
import html.parser as htmlparser

parser = htmlparser.HTMLParser()
users = {}
keyPhrase = "???"
active = False

def init():  
  pass


async def on_message(msg):
  global keyPhrase
  msg = await sanitize_input(msg)

    
  if (active and keyPhrase != "???" and msg.message.lower().find(keyPhrase.lower()) != -1 and msg.message[0] != C.command_char):
      await addToRaffle(msg, False)
  elif (not active and keyPhrase != "???" and msg.message.lower().find(keyPhrase.lower()) != -1):
      await B.send_message("No open raffle to join yet!")      

      
async def on_command(msg):
    global users
    global active
    global keyPhrase
  
    msg = await sanitize_input(msg)
    cmd = msg.message[1:].split(" ")
      

    if (cmd[0].lower() == "gatcha"):
        try:
            if (len(cmd) == 1):              
                if (active and keyPhrase != "???"):
                    await output_phrase()
                elif (active and keyPhrase == "???"):
                    await B.send_message("Oops! There's a raffle open, but there's no key phrase set! Kindly ask your host to set one using the '{0}{1} phrase' command!".format(msg.message[0], cmd[0]))
                else:
                    await B.send_message("There are no raffles open at this time.")
                    
                    
            elif (len(cmd) > 1):
                smallCmd = cmd[1].lower()
                print(smallCmd)
              
                if (smallCmd == "open"):
                    if (not active):
                        active = True
                        await B.send_message("Okay, guys! Get ready! The raffle's about to open again!")

                    if (keyPhrase == "???"):
                        await asyncio.sleep(1)
                        await B.send_message("Oh! Well. The raffle is open, but remember to set the key phrase using the '{0}{1} phrase' command!".format(msg.message[0], cmd[0]))
                    elif (keyPhrase != "???"):
                        await output_phrase()
                    else:
                        active = False
                        await B.send_message("Error in raffle state ({})! Closing raffle...".format(active))   
                      
                      
                elif (smallCmd == "close"):
                    if (active):
                        active = False
                        #keyPhrase = "???"
                        await B.send_message("The raffle is now closed!")
                    elif (not active):
                        await B.send_message("There are no open raffles to close!")
                    else:
                        await B.send_message("Error in raffle state ({})! Closing raffle...".format(active)) 

                      
                elif (smallCmd == "phrase"):
                    if (len(cmd) > 2):   
                        extraCmd = cmd[2:]
                        extraCmd = " ".join(extraCmd)

                        if (extraCmd != "???"):
                            keyPhrase = extraCmd
                            await B.send_message("NEW KEY PHRASE successfully registered!")
                            await output_phrase()
                        if (extraCmd == "???"):
                            await B.send_message("Sorry, the default value isn't a valid key phrase.")
                       
                    elif (len(cmd) == 2):
                        if (keyPhrase != "???"):
                            await output_phrase()
                        elif (keyPhrase == "???"):
                            await B.send_message("There is no key phrase at this time. Please set one using the '{0}{1} phrase' command!".format(msg.message[0], cmd[0]))                  
                        else:
                            print("Unexpected value for key phrase: {}".format(keyPhrase))                              
                      
                      
                elif (smallCmd == "reset"):
                    buffer = ""

                    if (len(users) > 0):
                        users = {}
                        buffer = "The list of raffle entrants has been reset "
                    else:
                        buffer = "The current list of raffle entrants is already empty "                    

                    if (keyPhrase != "???"):
                      keyPhrase = "???"
                      buffer += " AND its key phrase has been reset!"
                    elif (keyPhrase == "???"):
                      buffer += " BUT the key phrase remains blank."
                  
                    await B.send_message(buffer)
                  
                  
                elif (smallCmd == "list"):
                      if (len(users) > 0):
                          buffer = "[Current Raffle Entrants ({})]:".format(len(users))

                          for nerds in users:
                              buffer += " {} ,".format(nerds)

                          buffer = buffer.strip(",")

                          await B.send_message(buffer)

                      else:
                          await B.send_message("There are no entrants to list.")

                elif (smallCmd == "add"):
                    if (len(cmd) == 3):
                        await addToRaffle(cmd[2], True)                    
                    else:
                        await B.send_message("Improper inputs ({0})! Please try again using the format of: '{1}{2} <username>'".format(len(cmd), cmd[0], cmd[1]))
                                             
                else:
                    await B.send_message("Sorry, '{0}' is an invalid {1} command".format(cmd[1], cmd[0].lower()))
                      
        except:
            print("Error in gatcha.")
            print(sys.exc_info())
            pass


async def addToRaffle(msg, forced):
    global users
    global listRaw
      
    if (forced):
        print(msg)
        await B.request_user_list()        
        await asyncio.sleep(1)
        
        userRaw = self.user_list
        print(userRaw)

      
        if (userRaw != None): 
            print("User found!")
            username = userRaw.display_name
            numId = userRaw.user_id
        else:
            print("User not found. Inserting dummy user.")
            username = msg
            numId = 0
                                             
    else:    
        username = msg.display_name
        numId = msg.user_id
        
    for folks in users:
        if (folks == username):
            print(folks)
            await B.send_message("Looks like you're already in the raffle, @{}!".format(username))
            return
                                             
    users[username] = numId
    await B.send_message("@{} successfully joined the raffle!".format(username))


    

async def sanitize_input(msg):
  try:
    msg.message = parser.unescape(msg.message)
    return msg
  except:
    print("Sanitize error")
    
async def output_phrase():
    await asyncio.sleep(1)
    await B.send_message("The key phrase is: [ {} ]".format(keyPhrase))

'''             
"open":ok
"close":ok
"clear": ok
"help":
"spin": CRITICAL
"redo":
"phrase":ok
"add":
"remove":
"blacklist": 
"leave" (for participants)
cooldown system
persistent tracking
'''