# SPI_Analysis.py
# Function package for loading in SPI Data from BabyD

import os
import numpy as np

# general format of output``
# ! "Row0to1Data_NoPixelConnectedNumCaptures_1000_153837"
# ! "C:\Users\rif36645\OneDrive - Science and Technology Facilities Council\Projects-DESKTOP-P8841A7\DynamiX local files\testing_outputs\StephenTests\NoPixelSel\Row0to1Data_NoPixelConnectedNumCaptures_1000_153837.npy"

def load_data(filepath, framecapture = True, printkeys = False, printfilepaths = False, printfileinfo = False):
    """Collates recorded SPI data into a dictionary where each entry is a different row in the 16 x 16 pixel array.
    Can select between only reading in a partiular .npy file containing SPI data from 2 rows, or by setting "framecapture" to "True", 
    the full pixel array is loaded to dictionary from 8 .npy files which share a common testname. 

    Args:
        filepath (_type_): path of .npy file to be loaded in
        framecapture (bool, optional): Parameter which choses to load in all .npy files which share a common test name (True) or just the single specified file (False). 
        This is utilised to load all recorded SPI data which relates to the same test, producing a dictionary containing data for all rows of the pixel array. Defaults to True.
        printkeys (bool, optional): Prints the keys of the returned dictionary. Defaults to False.
        printfilepaths (bool, optional): Prints the file paths which were called in loading the data. This includes those that were identified to share a common test name. Defaults to False.
        printfileinfo (bool, optional): Prints the "filename", "test_name" and "RowID" as as split from the "filepath" argument. Used for debugging. Defaults to False.

    Returns:
        _type_: _description_
    """
    
    datastore = {} # can change to hdf5 later if I want
    filename = filepath.split('\\')[-1]
    RowID = filename.split('_')[0]
    test_name = filename.split('_')[1].split('NumCaptures')[0]
    if printfileinfo is True:
        print(filename)
        print(test_name)
        print(RowID)
    
    if framecapture is True: # look for other files that share the same name but different RowID to put together a frame of data
        capturefiles = []
        captureRowID = []
        capturetest_name = []
        for root, dirs, files in os.walk(filepath.split(filename)[0], topdown=True):
            for name in files:
                if test_name in name:
                    capturefiles += [os.path.join(root, name)]
                    captureRowID += [name.split('_')[0]]
                    capturetest_name += [name.split('_')[1].split('NumCaptures')[0]]

        filepaths = capturefiles.copy()
        RowIDs = captureRowID.copy()
        test_names = capturetest_name.copy()
    else:
        filepaths = [filepath]
        RowIDs = [RowID]
        test_names = [test_name]
        
    if printfilepaths is True:
        print(filepaths)
        
    for i in range(len(filepaths)):
        datastore[RowIDs[i] + test_names[i]] = np.load(filepaths[i])
    
    if printkeys is True:
        print(datastore.keys())
    return datastore

def calc_ave(datastore, buildarray = True):
    """Determines the average value for each pixel in the datastore, will accept the dictionary format produced by "load_data" or the numpy array format produced by "build_array".
    If in dictionary format the "buildarray" argument can be varied to return the output of this function either as a dictionary or a numpy array (array is default.)

    Args:
        datastore (_type_): Contains data from SPI array sweep in dictionary format OR in numpy array format
        buildarray (bool, optional): If "True", the output of this function is returned as a numpy array of shape (N,M) where N and M are the number of pixes in the x and y directions . Defaults to True.

    Returns:
        _type_: _description_
    """
    
    if isinstance(datastore, dict) is True:
        print('dictionary type datastore identified')
        
        ave_dict_fine = {}
        ave_dict_coarse = {}
        for key, item in datastore.items():
            
            fine1 = [np.average(item[0][:,pixel,1]) for pixel in range(16)]
            fine2 = [np.average(item[1][:,pixel,1]) for pixel in range(16)]
            ave_dict_fine['Fine' + key] = [fine1,fine2]
            
            coarse1 = [np.average(item[0][:,pixel,0]) for pixel in range(16)]
            coarse2 = [np.average(item[1][:,pixel,0]) for pixel in range(16)]
            ave_dict_coarse['Coarse' + key] = [coarse1,coarse2]
                
        if buildarray is True:
            array_fine = build_array(datastore = ave_dict_fine)
            array_coarse = build_array(datastore = ave_dict_coarse)
            return [array_fine, array_coarse]
        else:
            ave_dict = {**ave_dict_fine, **ave_dict_coarse}
            return ave_dict
        
        
    elif isinstance(datastore, np.ndarray) is True:
        print('numpy array type datastore identified')

        array_fine = np.average(datastore[:,:,:,1],axis=1)
        array_coarse = np.average(datastore[:,:,:,0],axis=1)  

        return [array_fine, array_coarse]
    
    else:
        print('unrecognised dataformat')


def build_array(datastore):
    """Converts dictionary containing SPI data for an the full detector array into numpy array of dimensions [16,N,16,3].
    Indexes 0 and 2 (shape = 16) define the number of pixels in the array
    Index 1 (shape = N) defines the number of frames collected
    Index 3 (shape = 3) selects between Coarse [0], Fine [1] and Overflow [2]

    Args:
        datastore (_type_): Contains data from SPI array sweep in dictionary format, argument is the output of "load_data"

    Returns:
        _type_: _description_
    """
    data_array = [[] for _ in range(16)] 
    for key, item in datastore.items():
        data_array[int(key.split('Row')[1].split('to')[0])] = item[0]
        data_array[int(key.split('Row')[1].split('to')[0]) + 1] = item[1]
        
    data_array = np.array(data_array)
    return data_array
        

## may be unnecessary
# def dark_correct(test_datastore, dark_dict): 
    
#     darkcorrected = {}
#     for k,v in dark_dict.items():
#         finekeys = []
#         if 'Fine' in k:
            
#             rowid = k.split('Fine')[1]
#             for kd, vd in test_datastore.items():
#                 if rowid in kd:
#                     vc = vd.copy()
#                     # vc0 = np.zeros(shape=(10000,16))
#                     # vc1 = np.zeros(shape=(10000,16))
#                     for i in range(len(vd[0][:,0,0])):
#                         vc[0][i,:,1] = vd[0][i,:,1] - [int(j) for j in v[0]]
#                         vc[1][i,:,1] = vd[1][i,:,1] - [int(j) for j in v[1]]
#                     darkcorrected[f'{kd}'] = vc
                    
#             finekeys += [k]
            
    
#     return darkcorrected

def paramsweep_loaddata(folderpath, ParamSweepStep = 1, pixel_select = 8, row_select = 0, AverageData = False): #! will improve later to allow for multiple pixels but not a priority rn
    """Loads in folder containing all of the data files for parameter sweep. By default returns an 4 dimensional array containing the sweep output: [N_captures,N_files,Npixels,3] 
    and a 1-D array containg the values of the sweeped parameter. The final index of the sweeped values returns the coarse data [0], fine data [1], or overflow value [2].
    With the "AverageData" argument set to "True" an additional variable will be returned which averages over the "N_captures" and calculates the standard deviation. 
    This is stored as an array of shape [2,N_files,N_pixels,3], where for first index Average is [0] and std = [1].
    
    **NOTE:** At current N_pixels is set to a specific pixel so retunring arrays will be 3-D not 4-D.

    Args:
        folderpath (_type_): _description_
        ParamSweepStep (int, optional): _description_. Defaults to 1.
        pixel_select (int, optional): _description_. Defaults to 8.
        row_select (int, optional): Can only take values 0 or 1 and correspond to the first or second row in the 2 row SPI readout file. For even numbered row, input 0, for odd numbered row, input 1. Defaults to 0.
        AverageData (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    
    ParentDatastore = []
    ParamSweeped = []

    for root, dirs, files in os.walk(folderpath, topdown=True):
        for file in files:
            datastore = load_data(filepath = folderpath + '/' + file, framecapture = False, printkeys = False)
            for key, item in datastore.items():
                ParamSweeped  += [int(file.split(f'step{ParamSweepStep}')[1].split('_')[0])]
                ParentDatastore += [item[row_select,:,:,:]] # row_select can only take values 0 or 1 and correspond to the first or second row in the 2 row SPI readout file.
                
    ParentDatastore = np.array(ParentDatastore)
    
    if isinstance(pixel_select, str):
        if pixel_select.lower == 'all':
            OrderedData = np.zeros_like(ParentDatastore[:,:,:,:]) # can only do this because step is 1
        else:
            print("invalid pixel selection, did you mean 'all', or a an index from 0 to 15?")
    else:
        OrderedData = np.zeros_like(ParentDatastore[:,:,pixel_select,:]) # can only do this because step is 1
    
    offset = int(file.split('start')[1].split('stop')[0])

    for i in range(len(ParamSweeped)):
        
        if isinstance(pixel_select, str):
            if pixel_select.lower == 'all':
                OrderedData[ParamSweeped[i] - offset,:,1] = ParentDatastore[i,:,:,1]# fine
                OrderedData[ParamSweeped[i] - offset,:,0] = ParentDatastore[i,:,:,0]# coarse
            else:
                print("invalid pixel selection, did you mean 'all', or a an index from 0 to 15?")
        else:
            OrderedData[ParamSweeped[i] - offset,:,1] = ParentDatastore[i,:,pixel_select,1]# fine
            OrderedData[ParamSweeped[i] - offset,:,0] = ParentDatastore[i,:,pixel_select,0]# coarse
        
        
    
    OrderedParamSweeped = sorted(ParamSweeped)
    
    if AverageData is False:
        return  OrderedParamSweeped, OrderedData
    
    else:   
        #* Average the readout over the number of captures and compute the standard deviation of the distribution
        AveStore = [np.average(OrderedData, axis = 1), np.std(OrderedData, axis = 1)]
        AveStore = np.array(AveStore) # has shape [2,N_files,N_pixels,3] where the first axis is: [0] = average across captures, [1] = standard deviation across captures

        
        return OrderedParamSweeped, OrderedData, AveStore
    
    
def twoparamsweep_loaddata(folderpath, SecondaryParamDirectories, returnraw = True):
    
    DataStore = {}
    
    for SecDir in SecondaryParamDirectories:
        subfolderpath = folderpath + '\\' + SecDir
        
        DataStore[SecDir + '_ys'], DataStore[SecDir + '_xs'] = paramsweep_loaddata(folderpath = subfolderpath, ParamSweepStep = 1, return_raw = returnraw)
    

    return DataStore




