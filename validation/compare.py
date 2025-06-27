from ionogram_visualizer import SimpleIonogramArrayBuilder
import ionread_python as ionread
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

ionogram = ionread.read_ionogram('../test_data/01_02_07_20_00.dat')
builder = SimpleIonogramArrayBuilder(ionogram).process()
ion_arr = builder.get_ndarray()


xtl, ytl = 70.44, 508-299.30
xbr, ybr = 154.27, 508-336.18


dpi = 100  
height, width = ion_arr.shape
fig_width = width / dpi
fig_height = height / dpi

fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=dpi)

im = ax.imshow(ion_arr, cmap='jet', origin='lower', aspect='auto')


rect = Rectangle((xtl, ytl),
                xbr - xtl, 
                ybr - ytl, 
                linewidth=2,
                edgecolor='r',
                facecolor='none')
ax.add_patch(rect)


plt.axis('off')
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # убираем все отступы


plt.savefig('ionogram_with_bbox.png', 
           bbox_inches='tight',
           pad_inches=0,
           dpi=dpi)
plt.close()
