import socket

#Global variables

SERVERPORT = 12492
HOSTADDR = "127.0.0.1"

# Chat Client class

class ChatClient:

    def __init__(self, port):
        self.port = port
        self.s = socket.socket()

    def run(self):
        self.s.connect((HOSTADDR, self.port))
        self.repeat = True
        self.login = ""
        while self.repeat:
            in_message = self.s.recv(1024)
            print in_message
            if in_message.startswith("Server: New user created. Now logged in to user "):
                self.login = in_message[48:(len(in_message) - 1)]
            elif in_message.startswith("Server: Now logged in to user "):
                self.login = in_message[30:(len(in_message) - 1)]
            self.userinput = raw_input(self.login + "> ")
            self.s.send(str(self.userinput))
            self.brokeninput = self.userinput.split(" ")
            if self.brokeninput[0] == "logout":
                self.repeat = False
                self.s.close()
            elif self.brokeninput[0] == "login":
                self.repeat = True
            elif self.brokeninput[0] == "send":
                self.repeat = True
            else:
                self.repeat = True


# Main program

chatClient = ChatClient(SERVERPORT)
chatClient.run()
