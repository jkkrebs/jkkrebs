#Code by Tyson Gates
#Version 1.1.0

#Requires numpy and matplotlib
#To use, put in same directory as working file and import LeastSquaresFit as lsf.
#Now, call the function plot(*insert array*)
#You may also add x-axis, y-axis, and title labels by calling the function plot(array,xlabel,ylabel,title) with the latter 3 arguments being optional strings.
#If you leave any of the last 3 arguments empty, they will be ignored with no consequence.

#DO NOT USE A LIST OF NUMPY ARRAYS
#IF YOU MAKE INDIVIDUAL NUMPY ARRAYS FOR X, Y, AND ERROR TO ADD TO A LIST, DO AS FOLLOWS: myVals.append(xVals.tolist())

import numpy as np
import matplotlib.pyplot as plt

def plot(vals,xlab="",ylab="",title=""):
    #array must have 3 subarrays with the first being x values, the second being y values, and the third being errors
    listPlot = plt.scatter(vals[0],vals[1])
    plt.errorbar(vals[0],vals[1],yerr=vals[2],fmt='o')
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.title(title)
    plt.show()
    numData = len(vals[0])
    #these vals lists are to gather the different values before they are later summed
    AAvals = []
    BBvals = []
    CCvals = []
    alphaVals = []
    betaVals = []
    gammaVals = []
    for i in range(0,numData,1):
        AAvals.append((vals[0][i]**2)/(vals[2][i]**2))
        BBvals.append(vals[0][i]/(vals[2][i]**2))
        CCvals.append(1/(vals[2][i]**2))

        alphaVals.append((vals[0][i]*vals[1][i])/((vals[2][i]**2)))
        betaVals.append((vals[1][i])/((vals[2][i])**2))
        gammaVals.append(((vals[1][i])**2)/((vals[2][i])**2))

    AA = sum(AAvals)
    BB = sum(BBvals)
    CC = sum(CCvals)
    DD = AA*CC-(BB**2)

    alpha = sum(alphaVals)
    beta = sum(betaVals)
    gamma = sum(gammaVals)

    m = ((CC*alpha)-(BB*beta))/DD
    b = ((-BB*alpha)+(AA*beta))/DD
    deltam = np.sqrt(CC/DD)
    deltab = np.sqrt(AA/DD)
    #can't add the letter chi or superscript, so chi squared is chisq and reduced chi squared is chisqred
    chisq = gamma-2*m*alpha-2*b*beta+(m**2)*AA+2*m*b*BB+(b**2)*CC
    chisqred = chisq/(numData-2)
    print("The best-fit slope is ",m," with uncertainty ",deltam)
    print("The best-fit intercept is ", b, " with uncertainty ", deltab)
    print("The reduced chi squared is ",chisqred)
    print("The best-fit velocity is ", 1/m)
    xVals = np.array(vals[0])
    yVals = m*xVals+b
    plt.errorbar(vals[0],vals[1],yerr=vals[2],fmt='o')
    plt.plot(xVals, yVals)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.title(title)
    plt.show()

#myVals = np.array([[1,2,3,4,5],[2.1,3.5,6.8,7.8,10.0],[.1,.3,.5,.7,.9]])
#plot(myVals)