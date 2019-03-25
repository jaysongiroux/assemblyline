"""
author: Jason Giroux, Matthew Ruch
Date: 3/22/2019
resources: Geeks for Geeks and Stackoverflow
notes:
this file reused a lot of methods from the 2 lane file. these methods were then adapted for the use of 3 lanes

"""
from numpy import loadtxt
import numpy as np
import numpy

"""
loadlines takes all of the textfiles and imports them into 2D arrays
"""
def loadlines():
    processtimes = loadtxt("ProcessTimes.txt")
    processtimestest = loadtxt("ProcessTimesTest.txt") #containing the time for each process
    ThreeLaneTransitions = loadtxt("ThreeLaneTransitions.txt")
    TwoLaneTransitions = loadtxt("TwoLaneTransitions.txt") #text file containing the transition time across production lines
    TwoLaneTransitionsTest = loadtxt("TwoLaneTransitionsTest.txt")
    return processtimes, ThreeLaneTransitions


""" this takes the array and converts to work with the assembly algorithm"""
def rearrange(a,b,c): #a = left, b=middle, c = right
    length = len(a) #determines length
    
    u=(3, length) #set up for 3 lanes -> defines 2d array
    u = np.zeros(u, dtype=int)

    for i in range(length): #left
        u[0][i]=int(a[i])
    for i in range(length):#middle 
        u[1][i]=int(b[i])
    for i in range(length): #right
        u[2][i]=int(c[i])
    print("rearranged: \n", u )
    return u


"""
- ignore the third col in processtime for two lanes [done]
- needs to be dynamically programmed
"""    
   
def Assembly (a, t, e, x): #a and t are 2d arrays with three lanes
    #counts length of a to determine the number of stations
    stationSize = len(a[0]) 
    
    #creates temp arrays to fill in loop later
    Temp1 = [0 for i in range(stationSize)] 
    Temp2 = [0 for i in range(stationSize)] 
    Temp3 = [0 for i in range(stationSize)]
      
    #leaving times  
    Temp1[0] = e[0] + a[0][0] 
    Temp2[0] = e[1] + a[1][0] 
    Temp3[0] = e[2] + a[2][0]
  
    # Fill tables Temp1[] and Temp2[] using 
    #min function is a simple comparison using an if statment
    
    """needs to be set up for three lanes"""
    for i in range(1, stationSize): 
        Temp1[i] = min(Temp1[i-1] + a[0][i],              #gets stuck at Temp1[5] + a[0][6], Temp2[5]+ t[1][6] + a[0][6]
                    Temp2[i-1] + t[1][i] + a[0][i],
                    Temp3[i-1] + t[2][i] + a[0][i])   #problem line needs to debug gets stuck at i =6
        Temp2[i] = min(Temp2[i-1] + a[1][i], 
                    Temp1[i-1] + t[0][i] + a[1][i],
                    Temp3[i-1] + t[2][i] + a[2][i])
        Temp3[i] = min(Temp3[i-1] + a[2][i],
                    Temp1[i-1] + t[0][i] + a[1][i],
                    Temp2[i-1] + t[1][i] + a[0][i])    #problem line [X] FIXED
  
    # consider exit times and return minimum and reutrns  
    return min(Temp1[stationSize - 1] + x[0], Temp2[stationSize - 1] + x[1],Temp3[stationSize -1]+x[2]) 


"""seperates 2d array into seperate arrays"""
def leftright(a):
    x = np.delete(a, -1, axis=1) #left
    x = np.delete(x, -1, axis=1) #left is done
    y = np.delete(a, -1, axis=1) #middle
    y = np.delete(y, -2, axis=1)
    z = np.delete(a, 0, axis=1 )#right
    z = np.delete(z,-2, axis=1)
    return x,y,z

     
#this method picks out the enter and exit times and removes them from the array by returning a new array
def enterexit(a): #used for two lanes for now
    length = 3
    enter = [0 for i in range(length)]
    exit = [0 for i in range(length)]
        
    enter[0] = a[0][0]
    enter[1] = a[0][1] #wil have to change when writing for three lanes
    enter[2] = a[0][2]
    exit[0] = a[1][0] 
    exit[1] = a[1][1]
    exit[2] = a[1][2]
    
    print("enter: \n",enter,"\n exit: \n", exit)
    return enter, exit
def removeenter(a):
    #print("before enter and exit removed: \n", a)
    b = a.tolist() #converts to python list from numpy array to use pop command
    #removes the enter and exit times since theyre passed independantly
    b[0].pop(0)
    b[0].pop(0)
    b[0].pop(0)
    b[1].pop(0)
    b[1].pop(0)
    b[1].pop(0)
    print("after enter and exit is removed: \n",b)
    return b

"""--------------------------------------------------------------------------------------------"""
 
#stores values from loadlines
processtimes,transitions = loadlines()

print("transitions: \n ", transitions) 
print("process times: \n", processtimes)

enter, exit = enterexit(processtimes) #done for three lanes
lleft,mmiddle, rright = leftright(transitions) #done with three lanes
left,middle ,right = leftright(processtimes) #done with three lanes
ll = rearrange(left,middle,right) #used for process time in assembly
ll = removeenter(ll) #done with three lanes
tt = rearrange(lleft, mmiddle,rright) #add zeros to\
print("total time after assembly: ", Assembly(ll, tt, enter, exit))



