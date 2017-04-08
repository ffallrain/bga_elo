#!/usr/bin/python
import sys,os
import random as rd 
import numpy as np
import math
import matplotlib.pyplot as plt

N_p = 100
K = 40

Strength_Scale = 120

players = np.array( range( N_p ) )

if False: 
    istrength = np.zeros( (N_p,) ) 
    for i in players:
        istrength[i] = rd.gauss(0,1.5) 
    avg = np.mean(istrength)
    istrength = (istrength - avg )*Strength_Scale + 1500

    ## log data
    ofp = open("players_elo.data",'w')
    for i in players:
        ofp.write("%g\n"%istrength[i])
    ofp.close()

else:
    istrength = np.array ( open("players_elo.data").readlines(), dtype=np.float32 )

# istrength = [ -1,1 ]

if False:
    elo = np.zeros( (N_p,) ) + 1500
else:
    elo = np.array( open("simulated_elo.data").readlines(), dtype = np.float32 )

### NOW SWITCH TO NEW 
if True:
    for i in players:
        if elo[i] < 1300 :
            elo[i] = 1300 


def run(i,j):

    ## Expectation
    p_iwin = 1.0/( 1+10**((istrength[j]-istrength[i])/400) )

    ## Simulation
    dice = rd.random()
    if dice < p_iwin : # i wins
        resulti,resultj = 1,0
    elif dice > p_iwin:               # j wins
        resulti,resultj = 0,1
    else:
        resulti,resultj = 0.5, 0.5   # Draw

    ## Analysis result
    pelo_iwin = 1.0/( 1+10**( (elo[j]-elo[i])/400 ) )
    diff = K*(resulti-pelo_iwin)

    if elo[i] < 1300 and diff < 0 :
        pass
    elif elo[i] > 1300 and elo[i] + diff < 1300:
        elo[i] = 1300 
    else:
        elo[i] = elo[i] + diff

    diff = - diff
    if elo[j] < 1300 and diff < 0 :
        pass
    elif elo[j] > 1300 and elo[j] + diff < 1300:
        elo[j] = 1300 
    else:
        elo[j] = elo[j] + diff

    return 

def avg_elo():
    return sum( elo ) / N_p
    
count_balance = 0
def balance():
    global count_balance 
    count_balance += 1
    print ">>>>> BALANCE START "
    bias = avg_elo() - 1500
    ratio = 1 - 1500/avg_elo()
    for i in players:
        dice = rd.random()
        if dice <= ratio : ## AFK, a new play is inserted
            print ">>>>> AFK ! old elo %8.0f, old istrength %8.0f ; "%(elo[i],istrength[i]),
            elo[i] = 1300
            istrength[i] = rd.gauss(0,1.5) * Strength_Scale + 1500 
            print "new elo %8.0f, new istrength %8.0f ."%(elo[i],istrength[i])
    print ">>>>> BALANCE FINISHED "
            

def one_game():
    ## count

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
    
    if flag :
        result = run(i,j)

    return flag  

def simulate( N ):
    i = 0 
    while True:
        result = one_game()
        if result :
            i += 1
        if i >= N :
            break

plt.figure(figsize=(9,9) )
if True:
    N = 500000
    avgs = list()
    games = range(N)
    for i in games :
        one_game()
        avgs.append( avg_elo() )
        if i%1000 == 0 :
            balance()


    plt.scatter( istrength,elo, color = 'g' , alpha = 0.5, label = "%d games played "%N )

    ## plot linear fit
    A = np.vstack( [istrength, np.ones(len(istrength))] ).T
    m,c = np.linalg.lstsq(A,elo)[0]
    x = np.linspace(1000,2200,1000)
    y = m*x+c
    plt.plot(x,y,color = 'g' ,label="y = %g*x%+g"%(m,c) ,linewidth=2)

    plt.legend(loc='best')
    plt.xlabel("Intrinsic Elo")
    plt.ylabel("Simulated Elo")
    plt.xlim( (1000,2100) )
    plt.ylim( (1000,2100) )

    plt.show()

