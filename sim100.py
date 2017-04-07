#!/usr/bin/python
import sys,os
import random as rd 
import numpy as np
import math
import matplotlib.pyplot as plt

N_p = 100
K = 40

Strength_Scale = 100

players = np.array( range( N_p ) )

istrength = np.zeros( (N_p,) ) 
for i in range(N_p):
    istrength[i] = rd.gauss(0,1) 
avg = np.mean(istrength)
istrength = (istrength - avg )*Strength_Scale + 1500

# istrength = [ -1,1 ]

elo = np.zeros( (N_p,) ) + 1500

def run(i,j):

    ## Expectation
    p_iwin = 1.0/( 1+10**((istrength[j]-istrength[i])/400) )

    ## Simulation
    dice = rd.random()
    if dice <= p_iwin : # i wins
        resulti,resultj = 1,0
    else:               # jwins
        resulti,resultj = 0,1

    ## Analysis result
    pelo_iwin = 1.0/( 1+10**( (elo[j]-elo[i])/400 ) )
    diff = K*(resulti-pelo_iwin)
    elo[i] = elo[i] + diff
    elo[j] = elo[j] - diff

    return (diff,  )
    

def process_one():
    ## count
    global total_count 

    ## random pick P
    i,j = rd.sample(players,2)

    ## would the g played?
    if True:
        dice = rd.random()
        diff_strength = abs(elo[i]-elo[j])
        criteria = math.exp( - diff_strength / 200. )
        if dice <= criteria :
            flag = True
        else:
            flag = False
    else:
        flag = True
    
    ## simulate
    if flag :
        result = run(i,j)
    else:
        result = 0,0

    ## output
    if flag:
        total_count += 1
        # print ">>>>> The %d game, winner get %8.3f elo"%(total_count,result[0])
        pass
    else:
        # print "----- refused"
        pass
    return result[0]

results = list()
def simulate( N ):
    for i in range(N):
        result = process_one()
        results.append(result)

total_count = 0
simulate(1000)
plt.scatter( istrength, elo, color = 'blue', alpha = 0.5, label = "1000" )

total_count = 0
simulate(10000)
plt.scatter( istrength, elo, color = 'green', alpha = 0.5, label = "10000" )

total_count = 0
simulate(100000)
plt.scatter( istrength, elo, color = 'yellow', alpha = 0.5, label = "100000" )

total_count = 0
simulate(1000000)
plt.scatter( istrength, elo, color = 'red', alpha = 0.5, label = "1000000" )

plt.legend(loc='best')

plt.show()


## linear regression
A = np.vstack( [e123, np.ones(len(e123))] ).T
m,c = np.linalg.lstsq(A,edirect)[0]
print m,c

## plot
plt.figure(figsize = (8,8))

x = np.linspace(-25,10,1000)
y = m*x+c
plt.plot(x,y,color = 'green',label="y = %g*x+%g"%(m,c) ,linewidth=2)
