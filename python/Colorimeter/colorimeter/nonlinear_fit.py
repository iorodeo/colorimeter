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
    maskPos = yFitDiff > 0
    indPos = ind[maskPos]
    indTrim = getLargestContiguousBlock(indPos)

    try:
        xFitTrim = xFit[indTrim]
        yFitTrim = yFit[indTrim]
    except IndexError:
        xFitTrim = xFit
        yFitTrim = yFit

    # Invert monotonic portion of polynomial fit using interpolation function
    interpFunc = scipy.interpolate.interp1d(yFitTrim, xFitTrim,kind='linear') 
    yFitMin = yFitTrim.min()
    yFitMax = yFitTrim.max()
    fitCoeff = (interpFunc, yFitMin, yFitMax)
    return fitCoeff, xFitTrim, yFitTrim
    

def getLargestContiguousBlock(ind):
    contiguousBlockList = []
    currentBlock = [ind[0]]
    for i in range(1,ind.shape[0]):
        diff = ind[i] - ind[i-1]
        if diff > 1:
            congituousBlockList.append(list(currentBlock))
            currentBlock = [ind[i]]
        else:
            currentBlock.append(ind[i])
    contiguousBlockList.append(currentBlock)
    sizeList = [(len(block),block) for block in contiguousBlockList]
    maxBlockSize, maxBlock = max(sizeList)
    return maxBlock


def getValueFromFit(fitCoeff,inputValue,numPts=500):
    interpFunc, minVal, maxVal = fitCoeff
    if (inputValue < minVal) or (inputValue > maxVal):
        raise ValueError, 'value outside of calibration range'
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


    



