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

if True: 
    istrength = np.array ( open("players_elo.data"  ).readlines(), dtype=np.float32 )
    elo       = np.array ( open("simulated_elo.data").readlines(), dtype=np.float32 )
    for i in players:
        if elo[i] < 1300 :
            elo[i] = 1300 

boyelo = 1200
boyistrength = 1987.05

def run(j):

    global boyelo
    global boyistrength

    ## Expectation
    p_iwin = 1.0/( 1+10**( (istrength[j]-boyistrength)/400 ) )

    ## Simulation
    dice = rd.random()
    if dice < p_iwin : # i wins
        resulti,resultj = 1,0
    elif dice > p_iwin:               # j wins
        resulti,resultj = 0,1
    else:
        resulti,resultj = 0.5, 0.5   # Draw

    ## Analysis result
    pelo_iwin = 1.0/( 1+10**( (elo[j]-boyelo)/400 ) )
    diff = K*(resulti-pelo_iwin)
    
    if boyelo < 1300 and diff < 0 :
        pass
    elif boyelo > 1300 and boyelo + diff < 1300 :
        boyelo = 1300 
    else:
        boyelo = boyelo + diff

    diff = - diff
    if elo[j] < 1300 and diff < 0 :
        pass
    elif elo[j] > 1300 and elo[j] + diff < 1300 :
        elo[j] = 1300 
    else:
        elo[j] = elo[j] + diff

    return 
    

def one_game():
    ## count
    global total_count 

    ## random pick P
    j = rd.sample(players,1)

    ## would the g played?
    if True:
        if True: # exponent
            dice = rd.random()
            diff_strength = abs(boyelo-elo[j])
            criteria = math.exp( - diff_strength / 200. )
            if dice <= criteria :
                flag = True
            else:
                flag = False
    
    result = run(j)

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
    total_count = 0
    for i in (20,20,20,40,40, ):
        color = colors.pop(0)
        simulate( i )
        
        ## plot elo
        plt.scatter( istrength,elo, color = color , alpha = 0.5, label = "%d games played "%total_count )

        ## plot linear fit
        A = np.vstack( [istrength, np.ones(len(istrength))] ).T
        m,c = np.linalg.lstsq(A,elo)[0]
        x = np.linspace(1000,2200,1000)
        y = m*x+c
        plt.plot(x,y,color = color ,label="y = %g*x%+g"%(m,c) ,linewidth=2)

        ## plot boy
        plt.scatter( (boyistrength,), (boyelo,), color = 'red', s = 100 , alpha = 0.5, )

    plt.legend(loc='best')
    plt.xlabel("Intrinsic Elo")
    plt.ylabel("Simulated Elo")
    plt.xlim( (1000,2100) )
    plt.ylim( (1000,2100) )

    plt.show()

