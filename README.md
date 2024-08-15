# BabyDPythonPackage
 Baby D Python Package containing data analysis and system simulation tools.

## Package contents:
1. **SPI_analysis.py** - module to provide functions for loading in and conducting basic analysis of SPI acquired data from the BabyD system.
2. **ChargeCancellationModel.py** - module for simulating an idealised version of the BabyD pixel architecture and predicting the readout based on selected bias settings and injected amount of charge.
3. **ExamplePlots.py** - module containg wrapper functions for generating common plots for consistency in design, layout and scheme.
4. **SerialisedData.py (WIP)**

## Package Installation & Setup
This repository has been designed as a python package which can be installed to your standard python distribution or virtual environment / conda environement. 

To do so, in the terminal locate yourself to the folder that this README.md file is present in, there should also be a `setup.py` file and the "BabyDTools" directory which contains the pacakge scripts.
This can be done by typing:
 `cd \Documents\Folder\Subfolder\BabyDPythonPackage`
where "Folder" and "Subfolder" are examples of the directories you may need to go through to reach the desired directory. Now you should be located in the correct file directory (you can type `dir` in the terminal to convince yourself).

### Installing to base python distribution
For a general installation of these packages into your base python distribtion utilise the Python pip installer and the `setup.py` fule. Enter the following into the command line:
`python -m pip install .`
The "." tells pip to install from the local directory you are in, it will automatically locate the `setup.py` file which it will use to install the correct package dependencies and build the package.

If python is not recognised / found try typing:
`C:\Users\<USER>\AppData\Local\Programs\python - m pip install .`
Where <USER> should be replaced by your log in name eg "rif36645"

### Installing to a virtual environment / conda environment
If you would instead like to install to a virtual environemnt or conda environment for those utilising Anaconda / Spyder you will first need to create the environment then install the package with the environment active.

This can be a bit confusing as it means that you wont be able to use this package all the time, only when you use the environment it is installed to as the active kernel, however, it is generally good practice to install custom pacakges to virtual environments in-case there are conflicting dependencies and it also keeps your base distribution a bit tidier.

#### Step 1: Creating the environement
To create a virtual environment you first locate to the folder you want to store your virtual enviroment in. It is often useful to either have a folder where you store all of them, or alternative create the enviroment in the directory where you intend to store your BabyD SPI data / analysis scripts.

Once you've cd'd to your desired directory enter into the command line:
`python -m venv <directory>`
Where directory is what you want to call the virtual enviroment, it is common to call virtual enviroments "venv".

The inbuilt `venv` module is available for Python versions 3.4+. If you are running an older version install the package `virtualenv` first via pip then use that to create your virtual environment.
`pip install virtualenv`; `virtualenv [directory]`.

Alternatively, for a conda environment, which is commonly used for systems and IDEs that utilise the anaconda distribution of Pyhton (if you use Spyder you are likely using anaconda) it works in a much similar way. FIrstly open the Anaconda Prompt (miniconda3) which shoud have come installed with Spyder and enter:
`conda create --name <environment name>`
**Note:** you should replace `<environment name>` with whatever you want to call your environment (make sure to remove the angled brackets "<",">"), something like "BabyD_Data_Env" is a good name in this instance.

#### Step 2: Activating the environment
To activate your virtual environment, within the command terminal, you locate yourself to the directory that your virtual environement (venv) is stored and enter:
`venv\Scripts\activate`
In the command line, next to where you type it should say (venv)

To deactivate the virtual environment you simply type `deactivate` into the command line.

To activate your conda environment, you again open the Anaconda Prompt (miniconda3) and type:
`conda activate <environment name>`
**NOTE:** for conda environments you do not need to specify a directory, this is because all conda environment are saved to a global folder in your Program Files.

`venv\python.exe -m pip install C:\Path\To\Package\BabyDPythonPackage\.`
This should install the 



