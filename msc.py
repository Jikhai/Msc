#!/usr/bin/python3
# Mini chat server

import os
import sys 
import socket
import select
import threading


def main():

    #if len(sys.argv) <2 :
        #print ("Usage : [link]")
        #sys.exit(1)

    #goal = sys.argv[1]
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
    
    clientlist = []

    while True : #tests avec nc localhost 7777

        socklist,list_a,list_b = select.select(clientlist + [lesocket],[],[])    
        
        for i in socklist : 
            if i == lesocket :
                established, addr = lesocket.accept()
                clientlist.append(established)
            else :
                texte=i.recv(1500)
                if len(texte) == 0 :
                    i.close()
                    clientlist.remove(i)
                else:
                    i.send(texte)
        output = 0
        #vérification du nombre de sockets ouverts.
        #for debug in clientlist : output += 1  
        #print ("------------------------------------\n", output)
    else : lesocket.close()


#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
    
    """try : 
        liste = socket.getaddrinfo(goal,"http",0,socket.SOCK_STREAM)
    except Exception as err:
        print("Failure ! -->", err)
        sys.exit(1)


    for a in liste :
        (family, type, proto, name, sockaddr) = a
        lesocket = socket.socket(family, type, proto)
    
        try :
            lesocket.connect(sockaddr)
        except Exception as err:
            print("Failure ! -->", err," :", sockaddr)
            continue

        break
    else:
        sys.exit(1)

        
    try :
        lesocket.send(b"GET /\r\n\r\n")
    except Exception as err:
        print("Failure ! -->", err)
        sys.exit(1)
    
    while True :
        if lesocket.recv(256) == b'' :
            break
        print(lesocket.recv(256))"""
