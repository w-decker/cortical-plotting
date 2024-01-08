#!/usr/bin env python

from nilearn import datasets, plotting
import nibabel as nib
import os
import matplotlib.pyplot as plt 
import numpy as np

def plot_hoc_label(roi: int, figtitle: str, axis: str or int, depth: int):
    """Plot label from Harvard Oxford Cortical-cortl-maxprob-thr50-1mm Atlas on 2d plane
    
    Parameters
    ----------
    atlas: nii file
        nibabel compatible Nifti file from Nilearn

    figtitle: str
        Title of resultant figure

    axis: str or int
        X(0), Y(1), or Z(2)

    depth: int
        How much

    Returns
    -------
    X: ndarray
        numpy ndarray for matplotlib.pyplot.imshow()
    """
    # parse some inputs
    if axis is str:
        if axis.lower() == 'x':
            axis = 0
        elif axis.lower() == 'y':
            axis = 1
        elif axis.lower() == 'z':
            axis = 2

    if depth is None:
        depth = 4
    
    # get atlas
    atlas = datasets.fetch_atlas_harvard_oxford("cortl-maxprob-thr50-1mm")

    # convert to array
    img = np.squeeze(nib.load(atlas["filename"]).get_fdata())

    # get some important img points
    img_size = img.shape
    extent = (img_size[0], 0,img_size[0], 0)
    d = img.shape[0]
    extent = (d, 0, d, 0)
    f = int(img_size[0]/depth)

    if axis is 0:
        parcel = img[f, :, :] == roi
        
        if roi not in img:
            raise ValueError(f'Incorrect ROI selection.\n Please select from the following:\n\
                             {np.unique(atlas["maps"].get_fdata())}')
        
        for i in range(f):
            plt.imshow(img[i, :, :], cmap='binary',  extent=extent)

        plt.imshow(parcel, alpha=0.8, cmap='viridis', extent=extent)

    elif axis is 1:
        parcel = img[:, f, :] == roi
    
        if roi not in img:
            raise ValueError(f'Incorrect ROI selection.\n Please select from the following:\n\
                                {np.unique(atlas["maps"].get_fdata())}')
        
        for i in range(f):
            plt.imshow(img[:, i, :], cmap='binary',  extent=extent)

        plt.imshow(parcel, alpha=0.8, cmap='viridis', extent=extent)

    elif axis is 2:
        parcel = img[:, :, f] == roi
    
        if roi not in img:
            raise ValueError(f'Incorrect ROI selection.\n Please select from the following:\n\
                                {np.unique(atlas["maps"].get_fdata())}')
        
        for i in range(f):
            plt.imshow(img[:, :, i], cmap='binary',  extent=extent)

        plt.imshow(parcel, alpha=0.8, cmap='viridis', extent=extent)



    plt.axis('off')
    plt.title(figtitle)

    return(parcel)

def surface_plot(roi, roi_name, hemi, brain_shape, colormap, dir, file_extension):
        """
        Plotting coritcal ROIs using Destrieux atlas for demonstration purposes.

        Arguments
        ------------------
        roi --> 
                type: integer
                use: ROI values based on Destrieux cortical parcellation. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2937159/
                example: roi=34 
        roi_name -->
                type: string
                use: Name of ROI. 
                example: 'angular gyrus'.
        hemi --> 
                type: string
                use: set left or right hemisphere
                example: hemi='left'
        brain_shape -->
                type: integer
                use: set brain shape to inflated (1) or pial (2)
                example: brain_shape=1
        colormap --> 
                type: string
                use: set colormap
                example: colormap='cyan_orange_r'
        dir -->
                type: string
                use: set directory for rendered plot
                example: dir='/Users/name/Desktop/
        file_extension --> 
                type: string
                use: define custom file extension for rendered plot
                example: file_extension='.png'

        Example
        ------------------
        surface_plot(roi=34, roi_name='stg', hemi='left', 
                brain_shape=2, colormap='cyan_orange_r', 
                dir='Users/name/Desktop/', 
                file_extension='.png')

        """

        # parse input arguments
        roi = roi
        roi_name = roi_name
        cmap = colormap
        dir = dir
        file_extension = file_extension

        if hemi.lower() == "left":
            hemi_atlas = 'map_left'
            hemi_shape = 'left'
        elif hemi.lower() == 'right':
            hemi_atlas = 'map_right'
            hemi_shape ='right'
        
        if brain_shape == 1:
             brain = 'infl'
        elif brain_shape == 2:
             brain = 'pial'

        # load in atlas
        atlas = datasets.fetch_atlas_surf_destrieux()

        # parcellation
        parcel = atlas[hemi_atlas]

        # get ROI and create mask
        roi = roi # change as needed
        mask = (parcel == roi)
        roi_name = roi_name

        # fsaverage
        fsaverage = datasets.fetch_surf_fsaverage()
        fscat = brain + '_' + hemi_shape

        # plot
        file2save = dir + roi_name + file_extension
        plotting.plot_surf_roi(fsaverage[fscat], roi_map=mask,
                                hemi=hemi_shape, view='lateral',
                                bg_map=fsaverage['sulc_left'], bg_on_data=True,
                                darkness=.5, cmap=cmap,
                                output_file=file2save)
        plotting.show()


