import socket
import thread

# Global variables

MAXCLIENTS = 3
LOGINFILE = "users.txt"
SERVERPORT = 12492

# Chat Server class
class ChatServer:

    # Initialize class
    def __init__(self, port):
        # Set port
        self.port = port

        # Create socket
        self.s = socket.socket()
        self.s.bind(("", port))
        self.s.listen(MAXCLIENTS)

        # Import logins
        file = open(LOGINFILE, "r")
        self.loginDictionary = {}
        for line in file:
            if line != "\n":
                loginInfo = line.split(",")
                loginID = loginInfo[0]
                loginPassword = loginInfo[1].rstrip()
                self.loginDictionary[loginID] = loginPassword
        print self.loginDictionary
        file.close()

    def run(self):
        print("Server running")
        self.connectionDictionary = {}
        # Start listening
        while True:
            c, addr = self.s.accept()
            print "Got connection from", addr
            c.send("Welcome to the chat room!")
            self.loginID = ""
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
                        if(self.loginDictionary[str(brokeninput[1])] == brokeninput[2]):
                            print "SUCCESSFUL LOGIN FROM", addr, "TO USER", brokeninput[1]
                            self.loginID = brokeninput[1]
                            c.send("Server: Now logged in to user " + self.loginID + ".")
                        else:
                            print "INVALID LOGIN FROM", addr
                            c.send("Server: Incorrect login.")
                        repeat = True
                    # SEND REQUEST
                    elif brokeninput[0] == "send":
                        if self.loginID != "":
                            c.send(self.loginID + ": " + message[5:])
                        else:
                            c.send("Server: Denied. Please login first.")
                    # NEWUSER REQUEST
                    elif brokeninput[0] == "newuser":
                        self.loginDictionary[str(brokeninput[1])] = brokeninput[2]
                        self.loginID = brokeninput[1]
                        file = open(LOGINFILE, "a")
                        file.write("\n" + brokeninput[1] + "," + brokeninput[2])
                        file.close()
                        c.send("Server: New user created. Now logged in to user " + self.loginID + ".")
                        repeat = True
                    # UNKNOWN REQUEST
                    else:
                        c.send("Server: Invalid request.")
                        repeat = True
                except:
                    c.send("Server: Invalid request.")

# Main program

chatServer = ChatServer(SERVERPORT)
chatServer.run()
