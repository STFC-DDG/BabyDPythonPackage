
import numpy as np
import matplotlib.pyplot as plt
import os

import SPI_analysis as SPI 
from ExamplePlots import histogram_pixel, CoarseFineCombinedPlot


#* Test 1 - Fine Stage Threshold

test1folder = r"\\te0dfs01\Datastores\HEXITECdata-mhz\BabyD\B16Device-ASICCharac - Test1"
OrderedParamSweeped, OrderedData = SPI.paramsweep_loaddata(folderpath = test1folder, ParamSweepStep = 1, pixel_select = 7, row_select=1, AverageData = False)

plt.figure()
plt.plot(OrderedParamSweeped, OrderedData[:,0,1])
plt.show()

#* Test 2 - Fine Stage Cancellation

#* Test 3 - Coarse Stage Threshold

#* Test 4 - Coarse Stage Cancellation
