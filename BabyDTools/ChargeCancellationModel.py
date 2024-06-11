#%%
def IDAC_to_Charge(CurrentMagnitude, InjectionClocks,  IDAC_ID = "IDACCal"):
    """Function to package the conversion from a DAC value to the associated amount of charge injected.
    This can be used from DAC values which represent either the magnitude of the current source applied or the 
    time duration it was applied for. Given the relationship is: Q = I * t, the order of the first two arguments
    is in fact irrelevant.

    Args:
        CurrentMagnitude (int): DAC value associated with the magnitude of the current source applied.
        InjectionClocks (int): Length of time in 2 ns clocks that the current source was active high for.
        IDAC_ID (str, optional): Takes values "IDACCal", "IDACCancel1" and "IDACCancel2" to specify one of the 3 current sources. Defaults to "IDACCal".

    Returns:
        Charge (float): The converted Charge value. Units given in coulombs (C).
    """

    # select current source - #TODO mirror down ratios will eventually need to be changed once have fully calibrated test pulse, could try and calibrate them to diamond data?
    if IDAC_ID.lower() == "idaccal": # idacCal
        MirrorRatio = 58.626534489359 # Mirror Down factor ### NEED TO UPDATE
        clockduration = 2.0e-9 # 2 ns
    elif IDAC_ID.lower() == 'idaccancel1': # idacCan1
        MirrorRatio = 27.37 ### NEED TO UPDATE
        clockduration = 3.0e-9 # 6 ns clock period but only high portion (3 ns) contributes to charge injection
    elif IDAC_ID.lower() == 'idaccancel2': # idacCan2
        MirrorRatio = 5937.36 ### NEED TO UPDATE
        clockduration = 12.0e-9 # 12 ns pulse
    else:
        print('incorrect IDAC ID selected, input a valid ID ("IDACCal", "IDACCancel1" or "IDACCancel2").')
        return 
    
    Charge = (CurrentMagnitude * 600e-6 * InjectionClocks * clockduration)/(4096 * MirrorRatio)
    return Charge

def Charge_to_Energy(Charge): #TODO Need to change this so that pair production energy can be selected for - defaulting to CZT 4.6
    """Function which packages the conversion of charge to energy for a specific detector material with a specified pair production energy. 
    At current build the CZT pair production energy is selected as default - to be made variable in future.
    Utilised with `IDAC_to_Charge()` function to determine the equivalent energy of the an injected pulse or charge cancellation when comparing with photon energy.

    Args:
        Charge (float): Charge value to be converted to the associated energy photon that would have produced it when absorbed by CZT. Units given in coulombs (C).

    Returns:
        Energy_eqv (float): The calculated energy equivalent charge for a CZT detector. Units given in electron volts (eV).
    """
    # constants
    pair_production = 4.64 # e-h pair production energy / eV
    e = 1.602e-19 # electron charge / C
    Energy_eqv = Charge * (pair_production/e) # equivalent energy in CZT (based on pair production energy)
    return Energy_eqv

def IDAC_to_Energy(CurrentMagnitude, InjectionClocks, IDAC_ID='IDACCal'):
    
    Charge = IDAC_to_Charge(CurrentMagnitude=CurrentMagnitude, InjectionClocks=InjectionClocks, IDAC_ID=IDAC_ID)
    Energy = Charge_to_Energy(Charge=Charge)
    
    return Energy

def Charge_to_CapacitorVoltage(Charge,Stage_Select):
    """Function which packages the conversion of charge to voltage stored on a capacitor of set capacitance.
    This is set to the values of the capacitors built into the 1st (Coarse) and 2nd (Fine) stages respectively - to be made adjustable in future.
    Utilised with `IDAC_to_Charge()` function to determine the equivalent voltage stored on the first or second stage capacitor due to an injected pulse or charge cancellation.

    Args:
        Charge (float): Charge value to be converted to a voltage stored on the selected stage capacitor. Units given in coulombs (C).
        Stage_Select (str): Selects between the 1st (Coarse) and 2nd (Fine) stages for calculating the associated voltage stored using the strings "1" and "2" respectively.

    Returns:
        Voltage_stored: The calculated voltage stored across the selected capacitor. Units given in volts (V).   
    """
    if Stage_Select == "1":
        Capacitance = 1.50e-13 # capacitance on first stage integrating capacitor / F
    elif Stage_Select == "2":
        Capacitance = 5.00e-14 # capacitance on second stage integrating capacitor / F
    else:
        print('Invalid stage selection, chose "1" for first stage (Coarse) and "2" for second stage (Fine).')
        return    
    
    Voltage_stored = Charge / Capacitance
    return Voltage_stored

def VDAC_to_voltage(VDAC, VrefAmp = False):
    """Function to package the conversion of a BabyD ASIC DAC setting to its respective generated voltage within the ASIC.
    This function is defaulted to assume the voltage you want to calculate is the one of the threshold voltages for the Coarse or Fine stage, however with the boolean argument
    "VrefAmp" = True the reference voltage is selected which as an additional offset voltage that needs to be accounted for.

    Args:
        VDAC (int): DAC settings defining the voltage generated within the ASIC for setting reference voltage of the pixel architecture or the Coarse/Fine stage threshold voltage.
                    Takes values between 0 and 4095.
        VrefAmp (bool, optional): Boolean argument which specifies if the voltage to be calculated is for one of the stage thresholds (False - Default) or the reference voltage of the pixel architecture (True).
                                In this scenario an additional offset = -304 mV is incldued to match the ASIC electronics. Defaults to False.

    Returns:
        voltage: The calculated voltage determined from the ASIC DAC setting input. Will either be related to the threshold voltage of one of the stages or the reference voltage for the pixel.
    """
    if VrefAmp is True:
        offset = -3.04e-1 # offset voltage in V needed for simulating VrefAmp voltage (-304 mV)
    else:
        offset = 0
    voltage = (VDAC * 1/4096) + offset  # the 1 is indicate 1 V which is the maximum voltage that the VDACs can set
    return voltage

def ChargeCancellation(VoltageStored, IDACCancel, VoutTH, Stage_Select, print_details = False):
    """Function which calculates the coarse or fine stage count based on cancellation voltage stored on the respective stage according to specified cancellation current ("IDACCancel") and threshold voltage (VoutTH) of the stage.
    Can select between the coarse and fine stage in which cancellation is occurring and the respective coarse or fine count (depending on "Stage_Select") is returned alongside any residual voltage.

    Args:
        VoltageStored (float): Voltage amount stored the 1st (Coarse) or 2nd (Fine) stage capacitor as selected by "Stage_Select". 
                            Utilised alongside `Charge_to_CapacitorVoltage()` for a particular injected charge or can be used with a generic input voltage. Units given in volts (V).
        IDACCancel (int): DAC setting defining the magnitude of the current part of the selected charge cancellation. The related charge is determined from `IDAC_to_Charge()` where again "Stage_Select" is used to 
                        specify which stage (Coarse / Fine) cancellation is calculated i.e. defining the pulse duration. Takes values between 0 and 4095.
        VoutTH (int): DAC setting defining the voltage generated within the ASIC for setting  the 1st (Coarse) or 2nd (Fine) stage threshold voltage as selected by "Stage_Select" and calculated from `VDAC_to_voltage()` Takes values between 0 and 4095.
        Stage_Select (str): Selects between the 1st (Coarse) and 2nd (Fine) stages for calculating the associated voltage stored using the strings "1" and "2" respectively.
        print_details (bool, optional): If set to be true then will print a statement saying that the specified "IDACCancel" and "VoutTH" values are the same as or differ from the default settings. 
                                        Default values are equivalent to 25 photons at 30 keV per Coarse Cancellation and 0.2 photons at 30 keV per Fine Cancellation. Defaults to False. #TODO implement a better way of doing this

    Returns:
        Count (int): The count associated with the number of times the selected stage's cancellation clock has fired - equivalent to X number of Y photons at Z keV.
        ResidualVoltage (float): Left over voltage post cancellation, utilised in simulation to propagate an injected charge through the 1st (Coarse) stage into the 2nd (Fine) stage.
    """
    
    ### Stage Specific parameters - set to be equivalent to 
    if Stage_Select == "1":
        default_IDACCancel = 1502
        default_VoutTH = 1763
        IDAC_ID = "IDACCancel1"
    elif Stage_Select == "2":
        default_IDACCancel = 919
        default_VoutTH = 1156 
        IDAC_ID = "IDACCancel2"
    else:
        print('Invalid stage selection, chose "1" for first stage (Coarse) and "2" for second stage (Fine).')
        return    
    
    # display if variation in the IDACCancel value supplied
    if print_details is True:
        if abs(default_IDACCancel - IDACCancel) > 0: 
            print(f"Selected non-default setting for IDACCancel: {IDACCancel} (default is {default_IDACCancel}).")
        else:
            print(f"Default setting for IDACCancel was selected: {IDACCancel}")

        if abs(default_VoutTH - VoutTH) > 0: 
            print(f"Selected non-default setting for VoutTH: {VoutTH} (default is {default_VoutTH}).")
        else:
            print(f"Default setting for VoutTH was selected: {VoutTH}")

    ### Calcualte voltage versions of the VDAC and IDAC settings to allow for comparisons with VoltageStored
    # define VoutTH1 in voltage
    V_VoutTH = VDAC_to_voltage(VoutTH)
    # define Voltage reduction upon a single clock of IDACCancel1
    V_IDACCan = Charge_to_CapacitorVoltage(Charge=IDAC_to_Charge(CurrentMagnitude = IDACCancel, InjectionClocks = 1,  IDAC_ID = IDAC_ID),Stage_Select=Stage_Select)

    Count = 0
    while VoltageStored >= V_VoutTH:
        VoltageStored -= V_IDACCan # Reduce voltage equivalent to the amount of charge discharge from capacitor upon incidence of IDACCancel1
        Count += 1 # increment coarse stage counter by 1
    
    ### pass any voltage < VoutTH as residual
    ResidualVoltage = VoltageStored
    assert ResidualVoltage < VoutTH, "Residual voltage has not been determined correctly, is larger than selected stage threshold"
    
    # return coarse count and residual voltage
    return Count, ResidualVoltage



def Readout(CurrentMagnitude, InjectionClocks, IDACCancel1 = 1502, VoutTH1 = 1763, IDACCancel2 = 919, VoutTH2 = 1156, print_details = False):
    """Function which simulated the readout of the Baby D detector for a specified amount of charge injected as defined by "CurrentMagnitude" and "InjectionClocks" passed through the `IDAC_to_Charge()` function.
    Default values are equivalent to 25 photons at 30 keV per Coarse Cancellation and 0.2 photons at 30 keV per Fine Cancellation, but this can be varied via the function arguments.

    Args:
        CurrentMagnitude (int): DAC value associated with the magnitude of the current source applied. In this case is particularly related to the test pulse current "IDACCal". Takes values between 0 and 4095.
        InjectionClocks (int): Length of time in 2 ns clocks that the current source was active high for.
        IDACCancel1 (int, optional): DAC setting defining the magnitude of the current part of the 1st (Coarse) stage charge cancellation. Takes values between 0 and 4095. Defaults to 1502.
        VoutTH1 (int, optional):  DAC setting defining the voltage generated within the ASIC for setting the 1st (Coarse) stage threshold voltage. Takes values between 0 and 4095. Defaults to 1763.
        IDACCancel2 (int, optional): DAC setting defining the magnitude of the current part of the 2nd (Fine) stage charge cancellation. Takes values between 0 and 4095. Defaults to 919.
        VoutTH2 (int, optional): DAC setting defining the voltage generated within the ASIC for setting the 2nd (Fine) stage threshold voltage. Takes values between 0 and 4095. Defaults to 1156.
        print_details (bool, optional): If set to be true then will print a statement saying that both "IDACCancel" and "VoutTH" values are the same as or differ from the default settings. Defaults to False. 

    Returns:
        ReadoutList (NDArray): Numpy array contain the coarse and fine counts relating to the specified injected charge. For multiple (N) values of "CurrentMagnitude" and "InjectionClocks" supplied, 
                                the equivalent dimension numpy array is returned with dim 2 in the zeroth axis (2,N).
    """
    import numpy as np
    # Check if test pulse input is not a single value, if not ensure it is in format that it can be correctly processed
        
    if isinstance(CurrentMagnitude,int) is True and isinstance(InjectionClocks,int) is True: 
        pass

    elif isinstance(CurrentMagnitude,int) is False and isinstance(InjectionClocks,int) is False: 
        if isinstance(CurrentMagnitude,list) is True:
            CurrentMagnitude = np.array(CurrentMagnitude)
        if isinstance(InjectionClocks,list) is True:
            InjectionClocks = np.array(InjectionClocks)

    else:

        if isinstance(CurrentMagnitude,int) is True:
            CurrentMagnitude = [CurrentMagnitude]*len(InjectionClocks)
            CurrentMagnitude = np.array(CurrentMagnitude)
            if isinstance(InjectionClocks,list) is True:
                InjectionClocks = np.array(InjectionClocks)
            assert len(CurrentMagnitude) == len(InjectionClocks), "Arguments are not of the same length."

        elif isinstance(InjectionClocks,int) is True:
            InjectionClocks = [InjectionClocks]*len(CurrentMagnitude)
            InjectionClocks = np.array(InjectionClocks)
            if isinstance(CurrentMagnitude,list) is True:
                CurrentMagnitude = np.array(CurrentMagnitude)
            assert len(CurrentMagnitude) == len(InjectionClocks), "Arguments are not of the same length."

        else:
            print("some other datainput type")
            print(type(CurrentMagnitude), type(InjectionClocks))


            
    ### Charge injected via test pusle circuit to mimic photon detection
    InjectedCharge = IDAC_to_Charge(CurrentMagnitude, InjectionClocks,  IDAC_ID = "IDACCal")

    ### Charge from test pulse is stored as a voltage on first stage capacitor
    VrefAmp = VDAC_to_voltage(VDAC = 2268, VrefAmp = True) 
    # need to add VefAmp to the voltage stored due to the injected charge as this is the baseline voltage
    VoltageStored_CoarseStage = Charge_to_CapacitorVoltage(InjectedCharge, Stage_Select = "1") + VrefAmp

    # First stage Cancellation #! note that the cancellation here is general and doesn't disguish between the second stage being a ramp adc and the first stage being a ? adc.
    if isinstance(VoltageStored_CoarseStage,float) is True:
        ReadoutDim = 1 # set dimensionality to 1 which can be used instead of length for incrementing
        VoltageStored_CoarseStage = [VoltageStored_CoarseStage] # turns float to a single valued list, measn we can use the generalised next step which accounts for cases with more than one input value
    else:
        ReadoutDim = len(VoltageStored_CoarseStage)
    ReadoutList = np.zeros(shape=(2,ReadoutDim))
    for vi in range(ReadoutDim):
        voltage = VoltageStored_CoarseStage[vi]
        CoarseCount, ResidualVoltage = ChargeCancellation(VoltageStored = voltage, IDACCancel = IDACCancel1, VoutTH = VoutTH1, Stage_Select = "1", print_details = print_details)
        # Residual Voltage is amplified by factor of 4 in transfer to fine stage - only that above the reference voltage is multiplied by 4
        Amp_ResidaulVoltage = ((ResidualVoltage - VrefAmp) * 4) + VrefAmp
        FineCount, DiscardedVoltage = ChargeCancellation(VoltageStored = Amp_ResidaulVoltage, IDACCancel = IDACCancel2, VoutTH = VoutTH2, Stage_Select = "2", print_details = print_details)
        
        ReadoutList[:,vi] = CoarseCount,FineCount

    return ReadoutList


# #%%  ###* Testing Area ###

# # need to calculate how much charge is equivalent to 0.25 of a 30 keV photon,  
# # what the threshold VDAC would be and what the cancellation IDAC should be?

# FineEnergy = 0.25 * 30 # 7.5 keV

# pair_production = 4.64 # ev / e-h pair production energy
# e = 1.602e-19 # electron charge / C

# FineCharge = (FineEnergy * 1000 * e) / pair_production # factor 1000 needed to convert from keV to eV

# # now we have charge we need to branch and calculate:
# # 1. Charge stored on fine stage capacitor -> VoutTH2
# FC2 = Charge_to_CapacitorVoltage(FineCharge/4,Stage_Select='2') # the divide by 4 is a guess
# print(FC2 + 0.00250)




# # 2. Charge cancelled on by fine stage cancel clock - IDACCancel2


# #%%

# # print(Readout(100,25,IDACCancel1=1502, IDACCancel2=1640, VoutTH1=1970, VoutTH2=1100))

# # I want to inject 1 coarse count which for the settings we want is equivalent to 25 photons at 30 keV

# print(IDAC_to_Energy(100,200)/(1000)) 


# # want to then vary voutTH1 until for the above IDACCal and TPP we get a fine output of 100 lsb + 3 lsb for dark correction

# print(Readout(100,54,IDACCancel1=1680, IDACCancel2=1200, VoutTH1=1750, VoutTH2=1030))


# print('Vrefamp = ', VDAC_to_voltage(2268, VrefAmp=True))
# print('VoutTH1 = ', VDAC_to_voltage(2268))
# print('VoutTH2 = ', VDAC_to_voltage(2268))