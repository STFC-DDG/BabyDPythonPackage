import numpy as np
from BabyDTools import ChargeCancellationModel as CCM
from BabyDTools.ExamplePlots import CoarseFineCombinedPlot


def DetectorReadout(ICal_I, ICal_F, PulseWidth, IDACCancel1 = 330, VoutTH1 = 1156, IDACCancel2 = 1178, VoutTH2 = 600, PrintDetails = False ):
    IDACCal = np.arange(ICal_I,ICal_F,PulseWidth)
    Time = np.ones(len(IDACCal)) * PulseWidth
    
    OutputA = CCM.Readout(CurrentMagnitude = IDACCal, InjectionClocks = Time, IDACCancel1 = 330, VoutTH1 = 1156, IDACCancel2 = 1178, VoutTH2 = 600, print_details = PrintDetails)
    CoarseFineCombinedPlot(OutputA[0], OutputA[1],IDACCal,xlabel='IDACCal Setting')

def PredictSettings():
    """
    Given specified coarse and fine count increment requirements, calculated predicted settings which fit this specification for an idea detector system.
    """
    
def CalibrationTestPulse():
    """
    For a required set number of fine counts and assocated increment energy resolution, 
    provide options for a test pulse which could be injected to produce such a fine count in an ideal detector.
    """