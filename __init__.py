from src import Bunn as B
import asyncio
import sys

users = []
keyPhrase = "???"
active = False

def init():  
  pass

async def on_command(msg):
    global users
    global active
    global keyPhrase
  
    cmd = msg.message[1:].split(" ")
    

    if (cmd[0] == "tombola"):
        try:
            if (len(cmd) == 1):              
                if (active and keyPhrase != "???"):
                    await B.send_message("Raffle currently running! The key phase is: {}".format(keyPhrase))
                elif (active and keyPhrase == "???"):
                    await B.send_message("There's a raffle open, but no key phrase to enter it!")
                else:
                    await B.send_message("There is no raffle open at this time.")
                    
                    
            elif (len(cmd) > 1):
              
                if (cmd[1] == "open"):
                  if (active):
                      await B.send_message("There is already an ongoing raffle!")
                  elif (not active):
                      active = True
                      await B.send_message("The raffle is now open for entry!")
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
                  print(len(cmd))
                  if (len(cmd) > 2):     
                        global cmd  
                      
                        extraCmd = cmd
                        print(extraCmd[0])
                        extraCmd.pop(0)
                        print(extraCmd[0])
                        extraCmd.pop(0)   
                        print(extraCmd[0])
                        cmd[2] = " ".join(extraCmd)
                        print(cmd)
                  if (len(cmd) == 2):
                      await B.send_message("There is no key phrase at this time. Please set one using the '{0}{1} phrase' command!".format(msg.message[0], cmd[0]))                  
                        
                  elif (cmd[2] and cmd[2] != "???"):
                      keyPhrase = cmd[2]
                      await B.send_message("The NEW KEY PHRASE to enter the raffle is now:      {}".format(cmd[2]))
                  elif (cmd[2] and cmd[2] == "???"):
                      await B.send_message("Sorry, the default value isn't a valid key phrase.")
                  elif (keyPhrase != "???"):
                      await B.send_message("The key phrase is currently:      {}.".format(keyPhrase))  
                      
                      
                
                else:
                    await B.send_message("Sorry, '{0}' is an invalid {1} command".format(cmd[1], cmd[0]))
        except:
            print("Error in tambola.")
            print(sys.exc_info())
            pass

  
  