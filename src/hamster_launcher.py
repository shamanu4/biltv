#!/usr/bin/python
import os

fa = 0
fb = 100

while fb<18000:
    print "new launcher thread %s-%s/17455" % (fa,fb)
    os.system('python run.py lib.functions "hamsters_swarm(%s,%s,0,100,0)"' % (fa,fb))
    fc = fb
    fb = fb*2-fa
    fa = fc
    
