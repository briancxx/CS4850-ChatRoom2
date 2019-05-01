# Lab 3 - Chat Room v2
# CS 4850
# Brian Cox
# 01 May 2019

import socket
import select
import sys

#Global variables

SERVERPORT = 12492
HOSTADDR = "127.0.0.1"

# Chat Client class

class ChatClient:

    # Class initializer, initialize port and socket
    def __init__(self, port):
        self.port = port
        self.s = socket.socket()

    # Run client program
    def run(self):
        # Connect to server
        self.s.connect((HOSTADDR, self.port))
        self.repeat = True
        self.login = ""
        # Repeat while logout request not called
        while self.repeat:
            # Formatting
            sys.stdout.write("> ")
            sys.stdout.flush()
            # Check for input from both client input and server
            read_sck, write_sck, err_sck = select.select([sys.stdin, self.s],[],[])
            for socks in read_sck:
                # Server message
                if socks == self.s:
                    # Show message to user
                    in_message = self.s.recv(1024)
                    print in_message

                    # Check if message is completed login, record user id
                    if in_message.startswith("Server: New user created. Now logged in to user "):
                        self.login = in_message[48:(len(in_message) - 1)]
                    elif in_message.startswith("Server: Now logged in to user "):
                        self.login = in_message[30:(len(in_message) - 1)]
                # Client input
                else:
                    # Collect input, send
                    self.userinput = raw_input()
                    self.s.send(str(self.userinput))

                    # Check if logout request
                    self.brokeninput = self.userinput.split(" ")
                    if self.brokeninput[0] == "logout":
                        # End program if logout request
                        self.repeat = False
                        self.s.close()
                    else:
                        self.repeat = True

# Main program

chatClient = ChatClient(SERVERPORT)
chatClient.run()
