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
clients = []

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
                c.close()
                repeat = False
            # LOGIN REQUEST
            elif brokeninput[0] == "login":
                print "LOGIN REQUEST FROM", addr
                print brokeninput[0], brokeninput[1], brokeninput[2]
                if(loginDictionary[str(brokeninput[1])] == brokeninput[2]):
                    print "SUCCESSFUL LOGIN FROM", addr, "TO USER", brokeninput[1]
                    loginID = brokeninput[1]
                    c.send("Server: Now logged in to user " + loginID + ".")
                else:
                    print "INVALID LOGIN FROM", addr
                    c.send("Server: Incorrect login.")
                repeat = True
            # SEND REQUEST
            elif brokeninput[0] == "send":
                if loginID != "":
                    c.send(loginID + ": " + message[5:])
                else:
                    c.send("Server: Denied. Please login first.")
            # NEWUSER REQUEST
            elif brokeninput[0] == "newuser":
                loginDictionary[str(brokeninput[1])] = brokeninput[2]
                loginID = brokeninput[1]
                file = open(LOGINFILE, "a")
                file.write("\n" + brokeninput[1] + "," + brokeninput[2])
                file.close()
                c.send("Server: New user created. Now logged in to user " + loginID + ".")
                repeat = True
            # UNKNOWN REQUEST
            else:
                c.send("Server: Invalid request.")
                repeat = True
        except:
            c.send("Server: Invalid request.")

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