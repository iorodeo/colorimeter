import numpy 

def getPolynomialFit(xList,yList,order=3,numPts=500): 
    """
    Compuetes the coefficient (slope of absorbance vs concentration)
    """
    coeff = numpy.polyfit(xList,yList,order)
    xFit = numpy.linspace(min(xList), max(xList), numPts)
    yFit = numpy.polyval(coeff, xFit)
    return coeff,xFit,yFit
