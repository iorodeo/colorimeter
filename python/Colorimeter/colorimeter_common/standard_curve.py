import numpy 

def getLinearFit(xList,yList,fitType='force_zero',numPts=500): 
    """
    Compuetes the coefficient (slope of absorbance vs concentration)
    """
    if fitType == 'force_zero': 
        xArray = numpy.array(xList)
        yArray = numpy.array(yList)
        numer = (xArray*yArray).sum()
        denom = (xArray*xArray).sum()
        slope = numer/denom
        xFit = numpy.linspace(min(xList), max(xList),numPts)
        yFit = slope*xFit
    else:
        polyFit = numpy.polyfit(xList,yList,1)
        xFit = numpy.linspace(min(xList), max(xList), numPts)
        yFit = numpy.polyval(polyFit, xFit)
        slope = polyFit[0]
    return slope,xFit,yFit
    

def getCoefficient(abso,conc,fitType='force_zero'):
    """
    Returns the calibration coefficient given absorbance and concentration
    values for a standard curve.
    """
    slope, dummy0, dummy1 = getLinearFit(abso,conc,fitType=fitType)
    return slope
