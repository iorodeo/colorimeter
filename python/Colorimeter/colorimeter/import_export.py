from __future__ import print_function
import os
import sys
import yaml
import time
import pkg_resources
import constants


def getUserTestSolutionDir(userHome): 
    return os.path.join(userHome,constants.USER_DATA_DIR)

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
        try:
            data = importTestSolutionData(name)
        except IOError, e:
            continue
        if data is None:
            continue
        if tag:
            key = '{0} ({1})'.format(data['name'],tag)
        else:
            key = data['name']
        testDict[key] = name
    return testDict

def loadUserTestSolutionDict(userHome,tag=''):
    """
    Load dictionary of test solution names to test solution data files.
    """
    userDir = getUserTestSolutionDir(userHome)
    fileList = getTestSolutionFilesFromDir(userDir)
    testDict = loadTestSolutionDict(fileList,tag=tag)
    return testDict

def loadDefaultTestSolutionDict(tag='D'):
    try:
        fileList = getTestSolutionFilesFromResources()
    except: 
        default_TestSolutionDir = getPyInstallerResourcePath('data')
        fileList = getTestSolutionFilesFromDir(default_TestSolutionDir)
    return loadTestSolutionDict(fileList,tag=tag)

def getTestSolutionFilesFromResources(): 
    fileNames = pkg_resources.resource_listdir('colorimeter','data')
    testFiles = []
    for name in fileNames:
        pathName = pkg_resources.resource_filename('colorimeter','data/{0}'.format(name))
        testFiles.append(pathName)
    return testFiles

def getPyInstallerResourcePath(relative_path): 
    # Old way - pyinstaller 1.5 
    #-------------------------------------------------------------
    #base_path = os.environ.get("_MEIPASS2", os.path.abspath("."))
    # New way - pyinstaller 2.0
    #-------------------------------------------------------------
    base_path = sys._MEIPASS
    resource_path = os.path.join(base_path, relative_path)
    return resource_path

def importTestSolutionData(fileName): 
    """
    Imports the test solution data with the given filename from the users
    test solutions directory.
    """
    with open(fileName,'r') as fid:
        data = yaml.load(fid)

    # For backward compatability
    if not 'fitType' in data:
        data['fitType'] = 'linear'
    if not 'fitParams' in data: 
        data['fitParams'] = None
    if (not 'concentrationUnits' in data) and (not 'units' in data):
        data['concentrationUnits'] = 'uM'
    if 'concentrationUnits' in data:
        data['units'] = data['concentrationUnits']
        del data['concentrationUnits']
    if data['fitParams'] in ('None', 'none'):
        data['fitParams'] = None
    return data

def exportTestSolutionData(userHome, dataDict): 
    """
    Exports test solution data to the users directory. Data is saved 
    as a yaml file.
    """
    solutionName = dataDict['name']
    fileName = getUniqueSolutionFileName(userHome, solutionName)
    with open(fileName,'w') as fid: 
        yaml.dump(dataDict,fid)

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

def getModeAndLEDTextFromData(data):
    """
    Returns mode and led from import file data.
    """
    if data is not None:
        isNewStyle = True 
        try:
            sensorMode = data['mode']
        except KeyError:
            isNewStyle = False 

        if isNewStyle:
            ledText = data['led']
        else:
            if data['led'] == 'custom':
                sensorMode = 'CustomLEDVerB'
                ledText = 'D1'
            else:
                sensorMode = 'StandardRGBLED'
                ledText = data['led']
        return sensorMode, ledText
    else:
        return None
