import socket
import select
import sys
from thread import *

# Global variables

MAXCLIENTS = 3
LOGINFILE = "users.txt"
SERVERPORT = 12492

server = None
loginDictionary = {}
clientDictionary = {}

# Initialize global variables
def serverInit(port):
    global server
    # Create socket
    server = socket.socket()
    server.bind(("", port))
    server.listen(MAXCLIENTS)

    # Import logins
    file = open(LOGINFILE, "r")
    for line in file:
        if line != "\n":
            loginInfo = line.split(",")
            loginID = loginInfo[0]
            loginPassword = loginInfo[1].rstrip()
            loginDictionary[loginID] = loginPassword
    print loginDictionary
    file.close()

# Create a client thread
def client(c, addr):
    print "Thread created for", addr
    c.send("Welcome to the chat room!")
    loginID = ""
    repeat = True
    while repeat:
        message = c.recv(1024)
        print "\"" + message + "\"", "from", addr
        brokeninput = message.split(" ")
        try:
            # LOGOUT REQUEST
            if brokeninput[0] == "logout":
                print "LOGOUT REQUEST FROM", addr
                if loginID != "":
                    sendToAll("Server", loginID + " has logged out.")
                    del clientDictionary[loginID]
                repeat = False
                c.close()
            # LOGIN REQUEST
            elif brokeninput[0] == "login":
                print "LOGIN REQUEST FROM", addr
                if loginID != "":
                    c.send("Server: Cannot switch users while logged in.")
                elif str(brokeninput[1]) not in clientDictionary:
                    if(loginDictionary[str(brokeninput[1])] == brokeninput[2]):
                        print "SUCCESSFUL LOGIN FROM", addr, "TO USER", brokeninput[1]
                        loginID = brokeninput[1]
                        clientDictionary[loginID] = c
                        c.send("Server: Now logged in to user " + loginID + ".")
                        sendToAllExcluding("Server", loginID, loginID + " has joined.")
                    else:
                        print "INVALID LOGIN FROM", addr
                        c.send("Server: Incorrect login.")
                    repeat = True
                else:
                    c.send("Server: User already logged in.")
            # SEND _ REQUEST
            elif brokeninput[0] == "send":
                print "SEND REQUEST FROM", addr
                if loginID != "":
                    if brokeninput[1] == "all":
                        print "SEND ALL REQUEST FROM", addr
                        sendToAll(loginID, message[9:])
                    elif brokeninput[1] in clientDictionary:
                        c.send(loginID + " (to " + brokeninput[1] + "): " + brokeninput[2])
                        clientDictionary[brokeninput[1]].send(loginID + " (to " + brokeninput[1] + "): " + brokeninput[2])
                    elif brokeninput[1] and brokeninput[2]:
                        c.send("Server: Please specify a logged-in recipient.")
                    else:
                        c.send("Server: Invalid request.")
                else:
                    c.send("Server: Denied. Please login first.")
            elif brokeninput[0] == "who":
                if loginID != "":
                    c.send(', '.join(list(clientDictionary.keys())))
                else:
                    c.send("Server: Denied. Please login first.")
            # NEWUSER REQUEST
            elif brokeninput[0] == "newuser":
                if str(brokeninput[1]) not in loginDictionary:
                    loginDictionary[str(brokeninput[1])] = brokeninput[2]
                    loginID = brokeninput[1]
                    file = open(LOGINFILE, "a")
                    file.write("\n" + brokeninput[1] + "," + brokeninput[2])
                    file.close()
                    clientDictionary[loginID] = c
                    c.send("Server: New user created. Now logged in to user " + loginID + ".")
                    sendToAllExcluding("Server", loginID, loginID + " has joined.")
                    repeat = True
                else:
                    c.send("Server: Error. User ID already exists.")
            # UNKNOWN REQUEST
            else:
                c.send("Server: Invalid request.")
                repeat = True
        except:
            c.send("Server: Invalid request.")

def sendToAll(fromID, message):
    for userID, client in clientDictionary.items():
        client.send(fromID + ": " + message)

def sendToAllExcluding(fromID, excludeID, message):
    for userID, client in clientDictionary.items():
        if userID != excludeID:
            client.send(fromID + ": " + message)


# Run server
def serverRun():
    print("Server running")
    # Start listening
    while True:
        c, addr = server.accept()
        print "Got connection from", addr
        start_new_thread(client, (c, addr))

# Main program

serverInit(SERVERPORT)
serverRun()
