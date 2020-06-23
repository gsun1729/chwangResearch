"""
    Written by Christine Hwang, chwang14@jhu.edu
    Created on 20200623
    
    This code contains two functions:
    
    1. convertID
    2. rewritefile
"""
import pandas as pd
import os

def convertID(filename1, filename2):
    '''
    This function reads in two csv files with the following end tags:
        1. "_newIds.csv"
        2. "_connections.csv"
    This function outputs a new csv file with the connections in the "_connections.csv"
    file converted to the old ID format specified in the "_newIds.csv" file.
    The new output csv file is named with "_connections_newId.csv' end tag.
    
    Parameters
    ===========
    filename1 : (string)
        Csv file name ending with "_newIds.csv"
    filename2 : (string)
        Csv file name ending with "_connections.csv"
    '''
    
    #grabbing base name for files
    basename = os.path.basename(filename2)
    wfile = basename[:-4] + '_newId.csv'
    
    #opening appropriate files
    newIdsdata = pd.read_csv(filename1, names=['Old ID'])
    connectionsdata = pd.read_csv(filename2, names=['ID1', 'ID2'])
    
    #grabbing row number and column number of connectionsdata
    rownum = connectionsdata.shape[0]

    #converting new ID format to old
    zerois = newIdsdata.iloc[0]
    for i in range(rownum):
        connectionsdata.at[i, 'ID1'] = connectionsdata.at[i, 'ID1'] + zerois
        connectionsdata.at[i, 'ID2'] = connectionsdata.at[i, 'ID2'] + zerois
    
    #writing output csv file with new name, changed data
    connectionsdata.to_csv(wfile, index = False, header = False)
    
def rewritefile(filename3):
    '''
    This function reads in a csv file with the following end tags:
        1. "_Volume"
    This function creates a pandas dataframe with data from the given csv file.
    
    Parameters
    ===========
    filename3 : (string)
        Csv file name ending with "_Volume.csv"
    '''
    
    #opening file
    volumedata = pd.read_csv(filename3, header = 2)
    print(volumedata.head())