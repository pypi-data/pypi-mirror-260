from nilearn.datasets import fetch_atlas_surf_destrieux, fetch_surf_fsaverage
from nilearn.plotting import plot_surf_roi, show
import numpy as np
import matplotlib.figure
import matplotlib.pyplot as plt

def plot_univariate(roi: list[int], cmap: str, 
                    shape: str = 'infl', hemi: str = 'left', 
                    view: str = 'lateral') -> matplotlib.figure.Figure:
    """Plot univariate brain
    
    Parameters
    ----------
    roi: list[int]
        Region(s) of interest defined by Destriuex atlas

    cmap: str
        Nilearn colormap

    shape: str
        Shape of brain surface
        Options: 'infl', 'pial'

    hemi: str
        Hemisphere
        Options: 'left' or 'l', 'right' or 'r'
    
    view: str
        which view
        Options: “lateral”, “medial”, “dorsal”, “ventral”,”anterior”, “posterior”

    Return
    ------
    P: matplotlib.figure.Figure
        Return matplotlib object
    """

    ATLAS = fetch_atlas_surf_destrieux()

    # parse args
    if hemi == "left":
        hemi_atlas = 'map_left'
        hemi_shape = 'left'
    elif hemi == 'right':
        hemi_atlas = 'map_right'
        hemi_shape ='right'

    # parcellation
    parcel = ATLAS[hemi_atlas]

    # get ROI and create mask
    mask = (parcel == roi)

    # fsaverage
    fsaverage = fetch_surf_fsaverage()
    fscat = shape + '_' + hemi_shape

    # plot
    P = plot_surf_roi(fsaverage[fscat], roi_map=mask,
                            hemi=hemi_shape, view=view,
                            bg_map=fsaverage[f'sulc_{hemi_shape}'], bg_on_data=True,
                            darkness=.5, cmap=cmap)

    return P

def plot_multivariate(roi: list[int], cmap: str,
                    shape: str = 'infl', hemi: str = 'left', 
                    view: str = 'lateral') -> matplotlib.figure.Figure:
    """Plot multivariate brain

    Parameters
    ----------
    roi: list[int]
        Region(s) of interest defined by Destriuex atlas

    cmap: str
        Nilearn colormap

    shape: str
        Shape of brain surface
        Options: 'infl', 'pial'

    hemi: str
        Hemisphere
        Options: 'left' or 'l', 'right' or 'r'
    
    view: str
        which view
        Options: “lateral”, “medial”, “dorsal”, “ventral”,”anterior”, “posterior”

    Return
    ------
    P: matplotlib.figure.Figure
        Return matplotlib object        
    """

    # atlas
    ATLAS = fetch_atlas_surf_destrieux()

    # get axes
    plt.cla()
    plt.axis('off')

    # parse args
    if hemi == "left":
        hemi_atlas = 'map_left'
        hemi_shape = 'left'
    elif hemi == 'right':
        hemi_atlas = 'map_right'
        hemi_shape ='right'

    #mask   
    hemi = ATLAS[hemi_atlas]
    mask = np.zeros_like(hemi, dtype=float)
    for i in roi:
        roi_indices = np.where(hemi == i)
        mask[roi_indices] = np.random.uniform(0.1, 10, size=len(roi_indices[0]))

    # fsaverage
    fsaverage = fetch_surf_fsaverage()
    fscat = shape + '_' + hemi_shape

    # Plot
    P = plot_surf_roi(fsaverage[fscat], roi_map=mask,
                                hemi=hemi_shape, view=view,
                                bg_map=fsaverage[f'sulc_{hemi_shape}'], bg_on_data=True,
                                darkness=0.5, cmap=cmap, figure=plt.gcf())
    
    
    return [P]

def plot_whole_multivariate(cmap: str,
                    shape: str = 'infl', hemi: str = 'left', 
                    view: str = 'lateral') -> matplotlib.figure.Figure:
    """Plot multivariate whole brain
    
    Parameters
    ----------
    cmap: str
        Nilearn colormap

    shape: str
        Shape of brain surface
        Options: 'infl', 'pial'

    hemi: str
        Hemisphere
        Options: 'left' or 'l', 'right' or 'r'
    
    view: str
        which view
        Options: “lateral”, “medial”, “dorsal”, “ventral”,”anterior”, “posterior”       

    Return
    ------
    P: matplotlib.figure.Figure
        Return matplotlib object
    """

    # get axes
    plt.cla()
    plt.axis('off')

    # atlas
    ATLAS = fetch_atlas_surf_destrieux()

    # parse args
    if hemi == "left":
        hemi_atlas = 'map_left'
        hemi_shape = 'left'
    elif hemi == 'right':
        hemi_atlas = 'map_right'
        hemi_shape ='right'

    # fsaverage
    fsaverage = fetch_surf_fsaverage()
    fscat = shape + '_' + hemi_shape

    #mask
    mask = np.zeros_like(ATLAS[hemi_atlas], dtype=float)
    mask = np.random.uniform(-10, 10, size=np.size(ATLAS[hemi_atlas]))

    #plot 
    P = plot_surf_roi(fsaverage[fscat], roi_map=mask,
                                hemi=hemi_shape, view=view,
                                bg_map=fsaverage[f'sulc_{hemi_shape}'], bg_on_data=True,
                                darkness=.5, cmap=cmap, figure=plt.gcf())
    
    return [P]