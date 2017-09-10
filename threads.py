#!/usr/bin/env python
# -*- coding: utf-8 -*-

# thread for malicious software 

import threading
import time, os, sys
from time import sleep

def worker(wait):
    for i in range(600):
        print wait
        time.sleep(600)

t = threading.Thread(target=worker,args=())
t.start()
#print "Hey, já se passou uma hora, mané!"
#print "Finalizando programa"
