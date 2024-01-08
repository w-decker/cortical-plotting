######## Plotting via brain_plotting.py for reproducibility ########

# import module
from brain_plotting import surface_plot, plot_hoc_label

# plot ROI on cortex
surface_plot(roi=34, roi_name='stg', hemi='left', brain_shape=1, 
             colormap='black_purple_r', dir='/Users/lendlab/Desktop/', file_extension='.png')

# plot ROI on 2d plane
plot_hoc_label(roi=15, figtitle='Test', axis='x', depth=None)