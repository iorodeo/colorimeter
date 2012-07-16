from __future__ import print_function
import os
import yaml

def getUserTestSolutionDir(userHome): 
    return os.path.join(userHome,'.iorodeo_colorimeter','data')

def getTestSolutionFilesFromDir(loc): 
    testFiles = os.listdir(loc) 
    testFiles = [name for name in testFiles if '.yaml' in name]
    testFiles = [os.path.join(loc,name) for name in testFiles]
    return testFiles

def loadTestSolutionDict(fileList,tag=''):
    """
    Creates test solutions dictionary from list of test solution
    files.
    """
    testDict = {}
    testFiles = [name for name in fileList if '.yaml' in name]
    for name in testFiles:
        data = importTestSolutionData(name)
        if data is None:
            continue
        if tag:
            key = '{0} ({1})'.format(data['name'],tag)
        else:
            key = data['name']
        testDict[key] = name
    return testDict

def loadUserTestSolutionDict(userHome):
    """
    Load dictionary of test solution names to test solution data files.
    """
    userDir = getUserTestSolutionDir(userHome)
    fileList = getTestSolutionFilesFromDir(userDir)
    testDict = loadTestSolutionDict(fileList)
    return testDict

def importTestSolutionData(pathName): 
    """
    Imports the test solution data with the given filename from the users
    test solutions directory.
    """
    try:
        with open(pathName,'r') as fid:
            data = yaml.load(fid)
    except IOError, e:
        print('Unable to read data file {0}'.format(name))
        print(str(e))
        data = None
    return data

def exportTestSolutionData(userHome, solutionName, dataList):
    """
    Exports test solution data to the users directory. Data is saved 
    as a yaml file.
    """
    filename = getUniqueSolutionFileName(userHome, solutionName)

def deleteTestSolution(userHome, solutionName):
    """
    Deletes test solution from user test solution directory.
    """
    testDict = loadUserTestSolutionDict(userHome)
    fileName = testDict[solutionName]
    os.remove(fileName)

def isUniqueSolutionName(userHome, solutionName):
    """
    Checks to see whether test solution name is unique.
    """
    testSolutionDict = loadUserTestSolutionDict(userHome)
    return solutionName not in testSolutionDict 

def isUniqueSolutionFileName(userHome,fileName):
    """
    Check whether or not filename for test solution is unique.
    """
    userDir = getUserTestSolutionDir(userHome)
    fileList = getTestSolutionFilesFromDir(userDir)
    return fileName not in fileList

def getUniqueSolutionFileName(userHome, solutionName):
    """
    Returns unique (human readable) filename for the given test solution 
    name.
    """
    testSolutionDir = getUserTestSolutionDir(userHome)
    fileNameBase  = "".join([x for x in solutionName if x.isalpha() or x.isdigit()])
    fileName = os.path.join(testSolutionDir, '{0}.yaml'.format(fileNameBase))
    done = False
    cnt = 0
    while not isUniqueSolutionFileName(userHome, fileName):
        cnt += 1
        fileName = os.path.join(testSolutionDir,'{0}_{1}.yaml'.format(fileNameBase,cnt))
    return fileName

