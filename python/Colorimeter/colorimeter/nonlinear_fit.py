import numpy 
import scipy.interpolate
import collections

def getPolynomialFit(xList,yList,order=3,numPts=500): 

    # Get unique x,y value pairs and sort
    valDict = {}
    for x,y in zip(xList,yList):
        try:
            valDict[x].append(y)
        except KeyError:
            valDict[x] = [y]

    for k,v in valDict.items():
        valDict[k] = numpy.mean(v)

    sortedVals = sorted(valDict.items())
    xSorted, ySorted = zip(*sortedVals)

    # Remove non monotonic parts of data
    xTrim, yTrim = [xSorted[0]], [ySorted[0]] 
    yLast = ySorted[0]
    for x,y in sortedVals[1:]:
        if y < yLast:
            break
        xTrim.append(x)
        yTrim.append(y)
        yLast = y

    # Fit data and remove any non-monotonic section  
    fitCoeff, xFit, yFit = polyFitThruZero(xTrim,yTrim,order,numPts) 
    ind = numpy.arange(yFit.shape[0])
    yFitDiff = yFit[1:] - yFit[:-1]
    maskNeg = yFitDiff < 0
    indNeg =ind[maskNeg]

    try:
        firstNeg= indNeg[0]
        xFitTrim = xFit[:firstNeg]
        yFitTrim = yFit[:firstNeg]
    except IndexError:
        xFitTrim = xFit
        yFitTrim = yFit

    # Invert monotonic portion of polynomial fit using interpolation function
    interpFunc = scipy.interpolate.interp1d(yFitTrim, xFitTrim,kind='linear') 
    yFitMin = yFitTrim.min()
    yFitMax = yFitTrim.max()
    fitCoeff = (interpFunc, yFitMin, yFitMax)
    return fitCoeff, xFitTrim, yFitTrim
    

def getValueFromFit(fitCoeff,inputValue,numPts=500):
    interpFunc, minVal, maxVal = fitCoeff
    if (inputValue < minVal) or (inputValue > maxVal):
        raise ValueError, 'input Value outside of interpolator range'
    outputValue = interpFunc(inputValue)
    return float(outputValue)


def polyFitThruZero(xList,yList,order,numPts):

    A = numpy.zeros((len(xList),order))
    xArray = numpy.array(xList)
    yArray = numpy.array(yList)
    for i in range(order):
        A[:,i] = xArray**(i+1)

    result = numpy.linalg.lstsq(A,yArray)
    coeff = result[0]

    xFit = numpy.linspace(min(xList), max(xList), numPts)
    AFit = numpy.zeros((numPts,order))
    for i in range(order):
        AFit[:,i] = xFit**(i+1)

    yFit = numpy.dot(AFit,coeff)

    return coeff, xFit, yFit


    



