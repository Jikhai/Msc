#!/usr/bin/python3
# Mini chat server

import os
import sys 
import socket
import select
import threading
import string


#Liste des sockets ouverts pour les clients
clientlist = []


def main():

    #if len(sys.argv) <2 :
        #print ("Usage : ")
        #sys.exit(1)
    try :
        lesocket = socket.socket(socket.AF_INET6,socket.SOCK_STREAM, 0)
    except Exception as err:
        print("Failure ! -->", err)
        sys.exit(1)

    lesocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    try :
        lesocket.bind(("",7777))
    except Exception as err:
        print("Failure ! -->", err)
        sys.exit(1)

    lesocket.listen(1)
    usrcount = 0

    notifjoin = ("Heads up everyone, a new user just entered the chatroom !\n").encode("utf-8")
    notifleave = ("Someone left.\n").encode("utf_8")
    greeting =("Welcome, please pick a username using the command : NICK <username> you can get a list of commands with HELP\n").encode("utf_8")
    
    while True : #tests avec nc localhost 7777

        socklist,list_a,list_b = select.select(clientlist + [lesocket],[],[])    
        for i in socklist : 
            if i == lesocket :
                established, addr = lesocket.accept()
                clientlist.append(established)
                usrcount +=1 
                print("one more user connected, total : ",usrcount) 
                established.send(greeting)
                for dest in clientlist :      
                        dest.send(notifjoin)
            else :
                text=i.recv(1500)
                if len(text) == 0 :
                    i.close()
                    clientlist.remove(i)
                    usrcount -=1
                    print("one user left : ", usrcount," left")
                    for dest in clientlist :      
                        dest.send(notifleave)
                else :
                    #i.send(text)
                    parse(text,i,chatfuncs)

        #vérification du nombre de sockets ouverts.
        #output = 0
        #for debug in clientlist : output += 1  
        #print ("------------------------------------\n", output)
    else : lesocket.close()

#-------------------------------------------------------------------------------
def message(text,emitter):
    text = text.encode("utf-8")
    for dest in clientlist :
        if dest != emitter :      
            dest.send(text)
            print ("a message was sent")

#------------------------------------------------------------------------------
#These functions here only use one parameter, and it's the recipient
def helpu(recipient): # *others lets you store additionnal arguments, but we'll use a try catch approach instead
    recipient.send(("lorem ipsum blablablah\n").encode("utf-8"))

#-------------------------------------------------------------------------------
def parse(text,recipient,chatfuncs):
    s = text.decode("utf-8")
    space = s.find(" ")
    if space == -1 : #  HELP doesn't take arguments,try checking for it before issuing an error message
        #notiferr(recipient) 
        s = s[:-1]
        if s in chatfuncsag :
            chatfuncsag[s](recipient)
            print("Command ", chatfuncsag[s]," was called")
        else :
            print("Unknown command called : ",s)
            notiferr(recipient)
    else :
        cmd = s[:space]
        if cmd in chatfuncs :
            chatfuncs[cmd](s[space+1:],recipient)
            print(chatfuncs[cmd]," was called")
        else :
            print("Unknown command called : ",cmd)
            notifunkn(recipient,cmd)
        #prints invoked command name in the console
        #print(s[:space])

#-------------------------------------------------------------------------------
def notiferr(recipient):
    recipient.send(("usage : COMMAND <args>, type HELP for more information\n").encode("utf-8"))
def notifunkn(recipient,cmd):
    recipient.send((cmd + " is not a known command, try HELP\n").encode("utf-8"))
#-------------------------------------------------------------------------------
#all the chat functions, 0 means not implemented yet
chatfuncs = {"MSG" : message, "NICK" : 0,"HELP": 0, "LIST" : 0, "KILL" : 0,"CHAN" : 0,"JOIN" : 0,"PART" : 0,"KICK" :0 }
#functions using only the "recipient" argument i.e. functions the user calls without argument   
chatfuncsag = {"HELP": helpu, "LIST" : 0, "CHAN": 0 }

#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
    
