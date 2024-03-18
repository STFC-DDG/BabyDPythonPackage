import matplotlib.pyplot as plt
import numpy as np
import os


def CoarseFineCombinedPlot(Coarse,Fine,xs,xlabel='DAC setting'):
    #### Needs to be adapted to allow for plotting of mutliple pixels on the same plot
    fig, ax1 = plt.subplots()

    assert len(Coarse) == len(Fine), 'Coarse and Fine data sets are not the same length'
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel('Fine Count', color = 'C0')
    ax1.tick_params(axis= 'y', labelcolor = 'C0')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Coarse Count', color = 'C1')
    ax2.tick_params(axis= 'y', labelcolor = 'C1')
    

    ax1.plot(xs,Fine,marker = 'o',markersize =3,mec = 'C0',mfc = 'none',linestyle ='-', linewidth = 1, alpha = 0.5, color = 'C0', label = 'Fine')
    ax2.plot(xs,Coarse,marker = 'o',markersize =3,mec = 'C1',mfc = 'none',linestyle ='-', linewidth = 1, alpha = 0.5, color = 'C1', label ='Coarse')

    fig.tight_layout()
    fig.legend(loc='upper center', bbox_to_anchor=(0.5, 1.06),
          ncol=3, fancybox=True, shadow=True)
    fig.show()

    return fig, ax1, ax2


def CoarseFineSubPlots(Coarse,Fine):
    fig, (ax1,ax2) = plt.subplots(ncols=1,nrows=2,sharex=True)

    ax1.plot(Coarse, color = 'C0', label ='Coarse')
    ax1.set_ylabel('Coarse Count', color = 'C0')
    ax1.tick_params(axis= 'y', labelcolor = 'C0')
    
    ax2.plot(Fine, color = 'C1', label = 'Fine')
    ax2.set_ylabel('Fine Count', color = 'C1')
    ax2.tick_params(axis= 'y', labelcolor = 'C1')
    ax2.set_xlabel('DAC setting')

    fig.tight_layout()
    plt.show()
    return fig, ax1, ax2


def histogram_array(array, plotcoarse = True, numslices = 5, limfine = False, limcoarse = True, save_plot = False, savedir = 'plots', plotname = None, return_data = False):
    """Takes in data array of format [xs,frames,ys,output_type] which has general shape of [16,N,16,3]

    Args:
        array (_type_): _description_
        plotcoarse (bool, optional): _description_. Defaults to True.
        numslices (int, optional): _description_. Defaults to 5.
        limfine (bool, optional): _description_. Defaults to False.
        limcoarse (bool, optional): _description_. Defaults to True.
        show_plots (bool, optional): _description_. Defaults to True.
        return_data (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    
    fig = plt.figure(figsize=(7,6))
    
    fineaves = []
    
    ax1 = fig.add_subplot(211)
    finebins = np.arange(0,2**7,1)

    if plotcoarse is True:
        
        coarseaves = []
        
        ax2 = fig.add_subplot(212) # add subplot for showing coarse data
        coarsebins = np.arange(0,2**8,1)
    
    numframes = len(array[0,:,0,0]) # number of collections / frames in data array
    slicewidth = int(numframes/numslices)

    for i in range(numslices):
        fineave = np.average(array[:,i:i*slicewidth+slicewidth,:,1],axis=1)
        
        ax1.hist(fineave.ravel(),finebins,label=f'time {i}')
        
        fineaves += [fineave]
        
        if plotcoarse is True:
            coarseave = np.average(array[:,i:i*slicewidth+slicewidth,:,0],axis=1)    
        
            ax2.hist(coarseave.ravel(),coarsebins,label=f'time {i}')
            
            coarseaves += [coarseave]
    
    ax1.legend()
    ax1.set_xlabel('Fine Count')
    ax1.set_ylabel('Frequency')
    if limfine is True:
        ax1.set_xlim(-0.25,max(fineave.ravel()) + 1.25)  # some "white space" is added around the data extremes to make plot better to look at
    
    
    if plotcoarse is True:    
        ax2.legend()
        ax2.set_xlabel('Coarse Count')
        ax2.set_ylabel('Frequency')
        
        if limcoarse is True:
            ax2.set_xlim(-0.25,max(coarseave.ravel()) + 1.25)


    if save_plot is True:
        
        # check if plots folder exists
        if not os.path.exists(savedir):
            os.makedirs(savedir)
        
        if plotname is None:
            fig.savefig(savedir + '\\ArrayHistogram.png')
        else:
            fig.savefig(savedir + f'\\ArrayHistogram_{plotname}.png')
    
    if return_data is True:
        return fineaves, coarseaves
    
def histogram_pixel(array, pixel_sel = (8,8), plottitle = 'Histogram of Pixel Output', plotcoarse = True, print_std = True, set_limfine = False, limfine = (0,128), set_limcoarse = False, limcoarse = (0,256), save_plot = False, savedir = 'plots', plotname = None):
    
    fig = plt.figure(figsize=(7,6))

    ax1 = fig.add_subplot(211)
    finebins = np.arange(0,2**7,1)
    ax1.hist(array[pixel_sel[1],:,pixel_sel[0],1],finebins,label=f'pixel ({pixel_sel[0]},{pixel_sel[1]})')

    ax1.legend()
    ax1.set_xlabel('Fine Count')
    ax1.set_ylabel('Frequency')
    if set_limfine is True:
        ax1.set_xlim(limfine[0],limfine[1])  # some "white space" is added around the data extremes to make plot better to look at
    
    if plotcoarse is True:
    
        ax2 = fig.add_subplot(212) # add subplot for showing coarse data
        coarsebins = np.arange(0,2**8,1)
        ax2.hist(array[pixel_sel[1],:,pixel_sel[0],0],coarsebins,label=f'pixel ({pixel_sel[0]},{pixel_sel[1]})')

        ax2.legend()    
        ax2.set_xlabel('Coarse Count')
        ax2.set_ylabel('Frequency')
        
        if set_limcoarse is True:
            ax2.set_xlim(limcoarse[0],limcoarse[1])
    
    if save_plot is True:
        
        # check if plots folder exists
        if not os.path.exists(savedir):
            os.makedirs(savedir)
        
        if plotname is None:
            fig.savefig(savedir + f'\\Pixel({pixel_sel[0]},{pixel_sel[1]})Histogram.png')
        else:
            fig.savefig(savedir + f'\\Pixel({pixel_sel[0]},{pixel_sel[1]})Histogram_{plotname}.png')
    
    if print_std is True:
        print('Fine Stage Standard Deviation for pixel (8,8) = ',np.std(array[pixel_sel[0],:,pixel_sel[1],1]))
        print('Coarse Stage Standard Deviation for pixel (8,8) = ',np.std(array[pixel_sel[0],:,pixel_sel[1],0]))