"""
    Written by Christine Hwang, chwang14@jhu.edu
    Created on 20200623
    
    This code contains two functions:
    
    1. convertID
    2. rewritefile
"""
import pandas as pd
import os

def convertID(fileName1, fileName2):
    '''
    This function reads in two csv files with the following end tags:
        1. "_newIds.csv"
        2. "_connections.csv"
    This function outputs a new csv file with the connections in the "_connections.csv"
    file converted to the old ID format specified in the "_newIds.csv" file.
    The new output csv file is named with "_connections_newId.csv' end tag.
    
    Parameters
    ===========
    fileName1 : (string)
        Csv file name ending with "_newIds.csv"
    fileName2 : (string)
        Csv file name ending with "_connections.csv"
        
    Outputs
    ===========
    Writes a csv file, name ending with "_connections_newId.csv", to disk
    No returns
    '''
    
    #grabbing base name for files
    baseName, extension = os.path.splitext(fileName2)
    
    #making output csv file new name
    wFile = baseName + '_newId.csv'
    
    #opening appropriate files
    newIdsData = pd.read_csv(fileName1, names=['Old ID'])
    connectionsData = pd.read_csv(fileName2, names=['ID1', 'ID2'])
    
    #grabbing row number of connectionsData
    connectionRow = connectionsData.shape[0]

    #converting new ID format to old
    firstId = newIdsData.iloc[0]
    for i in range(connectionRow):
        connectionsData.at[i, 'ID1'] = connectionsData.at[i, 'ID1'] + firstId
        connectionsData.at[i, 'ID2'] = connectionsData.at[i, 'ID2'] + firstId
    
    #writing output csv file with new name, changed data
    connectionsdata.to_csv(wFile, index = False, header = False)
    

def rewritefile(volumeFile):
    '''
    This function reads in a csv file with the following end tags:
        1. "_Volume"
    This function creates a pandas dataframe with data from the given csv file.
    
    Parameters
    ===========
    volumeFile : (string)
        Csv file name ending with "_Volume.csv"
        
    Outpus
    ===========
    No returns
    '''
    
    #opening file
    volumeData = pd.read_csv(volumeFile, header = 2)