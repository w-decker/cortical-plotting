#!/usr/bin env python

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

        from nilearn import datasets, plotting
        import os

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


