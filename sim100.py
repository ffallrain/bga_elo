#!/usr/bin/python
import sys,os
import random as rd 
import numpy as np
import math
import matplotlib.pyplot as plt

N_p = 100
K = 20

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

elo = np.zeros( (N_p,) ) + 1500

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
    elo[i] = elo[i] + diff
    elo[j] = elo[j] - diff

    return (diff,  )
    

def one_game():
    ## count
    global total_count 

    ## random pick P
    i,j = rd.sample(players,2)

    ## would the g played?
    if True:
        if True: # exponent
            dice = rd.random()
            diff_strength = abs(elo[i]-elo[j])
            criteria = math.exp( - diff_strength / 200. )
            if dice <= criteria :
                flag = True
            else:
                flag = False
        else:
            diff_strength = abs(elo[i]-elo[j])
            if diff_strength > 200 :
                flag = False
            else:
                flag = True
            
    else:
        flag = True
    
    result = run(i,j)

    ## output
    if flag:
        total_count += 1
        # print ">>>>> The %d game, winner get %8.3f elo"%(total_count,result[0])

    return 

def simulate( N ):
    for i in range(N):
        one_game()


if True: ## main

    plt.figure(figsize=(9,9) )

    colors = ['g','r','b','black','purple']
    for i in (200000, ):
        color = colors.pop(0)
        total_count = 0
        simulate( i )
        
        ## log simulated elo
        ofp = open("simulated_elo.data",'w')
        for i in players:
            ofp.write("%g\n"%elo[i])
        ofp.close()
        
        ## plot elo
        plt.scatter( istrength,elo, color = color , alpha = 0.5, label = "%d games played "%total_count )

        ## plot linear fit
        A = np.vstack( [istrength, np.ones(len(istrength))] ).T
        m,c = np.linalg.lstsq(A,elo)[0]
        x = np.linspace(1000,2200,1000)
        y = m*x+c
        plt.plot(x,y,color = color ,label="y = %g*x%+g"%(m,c) ,linewidth=2)

    plt.legend(loc='best')
    plt.xlabel("Intrinsic Elo")
    plt.ylabel("Simulated Elo")
    plt.xlim( (1000,2100) )
    plt.ylim( (1000,2100) )

    plt.show()

