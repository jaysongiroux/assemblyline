"""
author: Jason Giroux, Matthew Ruch
Date: 3/22/2019
resources: Geeks for Geeks and Stackoverflow

"""
from numpy import loadtxt
import numpy as np
import numpy

"""
loadlines takes all of the textfiles and imports them into 2D arrays
will not be included in the timing of this problem
"""
def loadlines():
    processtimes = loadtxt("ProcessTimes.txt")
    processtimestest = loadtxt("ProcessTimesTest.txt") #containing the time for each process
    ThreeLaneTransitions = loadtxt("ThreeLaneTransitions.txt")
    TwoLaneTransitions = loadtxt("TwoLaneTransitions.txt") #text file containing the transition time across production lines
    TwoLaneTransitionsTest = loadtxt("TwoLaneTransitionsTest.txt")
    #return processtimestest, TwoLaneTransitionsTest
    return processtimes, TwoLaneTransitions


""" this takes the array and converts to work with the assembly algorithm"""
def rearrange(a,b):
    length = len(a)
    u=(2, length) #set up for 2 lanes 
    u = np.zeros(u, dtype=int)
    #print("u: ",u) #prints the array filled with zeros to declare it
    #print("a: ",a)
    #print("b: ",b)
    for i in range(length):
        u[0][i]=int(a[i])
        #print("u: ",u[0][i])
    for i in range(length):
        u[1][i]=int(b[i])
    print("rearranged: \n", u )
    return u


"""
- ignore the third col in processtime for two lanes [done]
- needs to be dynamically programmed
"""    
def min(a,b):
    if a>b: 
        return b
    else:
        return a
    
def Assembly (a, t, e, x): 
    #counts length of a to determine the number of stations
    stationSize = len(a[0]) 
    
    #creates temp arrays to fill in loop later
    Temp1 = [0 for i in range(stationSize)] 
    Temp2 = [0 for i in range(stationSize)] 
      
    #leaving times  
    Temp1[0] = e[0] + a[0][0] 
    Temp2[0] = e[1] + a[1][0] 
  
    # Fill tables Temp1[] and Temp2[] using 
    #min function is a simple comparison using an if statment
    for i in range(1, stationSize): 
        Temp1[i] = min(Temp1[i-1] + a[0][i],              #gets stuck at Temp1[5] + a[0][6], Temp2[5]+ t[1][6] + a[0][6]
                    Temp2[i-1] + t[1][i] + a[0][i])   #problem line needs to debug gets stuck at i =6
        Temp2[i] = min(Temp2[i-1] + a[1][i], 
                    Temp1[i-1] + t[0][i] + a[1][i])    #problem line [X] FIXED
  
    # consider exit times and return minimum and reutrns  
    return min(Temp1[stationSize - 1] + x[0], Temp2[stationSize - 1] + x[1]) 
   
"""removes last col of array"""
def threecoltotwo(a):
    #uses numpy to remove a col
    
    b = np.delete(a, -1, axis=1)
    #print("three to two \n",b)
    return b


"""seperates 2d array into seperate arrays"""
def leftright(a):
    x = np.delete(a, -1, axis=1)
    y = np.delete(a,-2,axis=1)
    #print("Process times left: \n",x) #col left
    #print("Process times right: \n",y) #col right
    return x,y
    
#this method picks out the enter and exit times and removes them from the array by returning a new array
def enterexit(a): #used for two lanes for now
    enter = [0,0]
    exit = [0,0]    
    enter[0] = a[0][0]
    enter[1] = a[0][1] #wil have to change when writing for three lanes
    exit[0] = a[1][0] 
    exit[1] = a[1][1]
    
    print("enter: \n",enter,"\n exit: \n", exit)
    return enter, exit
def removeenter(a):
    #print("before enter and exit removed: \n", a)
    b = a.tolist() #converts to python list from numpy array to use pop command
    #removes the enter and exit times since theyre passed independantly
    b[0].pop(0)
    b[0].pop(0)
    b[1].pop(0)
    b[1].pop(0)
    print("after enter and exit is removed: \n",b)
    return b

    
"""--------------------------------------------------------------------------------------------"""
 
#stores values from loadlines
processtimes,transitions = loadlines()
processtimes = threecoltotwo(processtimes) #converts to two cols for easier navigation
#processtimes = rearrange(processtimes)
print("transitions: \n ", transitions) 
print("process times: \n", processtimes)
#print(processtimes[3][0])
enter, exit = enterexit(processtimes)
lleft, rright = leftright(transitions)
left, right = leftright(processtimes)
ll = rearrange(left,right) #used for process time in assembly
ll = removeenter(ll)
print("transitions: ")
tt = rearrange(lleft, rright) #add zeros to

print("time: ", Assembly(ll, tt, enter, exit)) #process time, trans time, enter, exit



