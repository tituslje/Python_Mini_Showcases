import seaborn as sns
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np


def plot_colour_legend(input_data):
    #generates the colour legend for plots with unique configs <= 5
    
    #config_data should be the list of lists generated after the Omega code. Each list should be 13 length representing pressures 0 - 12, and T lists representing number of temperatures considered
    
    #this function is called inside heatmap_plot_legendonly()
    
    unique_config_names = set([item for sublist in input_data for item in sublist])
    labels_legend = list(unique_config_names)
    
    color_legend = ['blue','pink','yellow'] #hardcoded for now
    
    handles_legend = [Rectangle((0,0),1,1,color=color) for color in color_legend]
    
    return plt.legend(handles_legend,labels_legend,title='O* Coverages',loc='upper right',bbox_to_anchor=(1.1,1))


def heatmap_plot_legendonly(config_data,tempture_list):
    #input data, config_data should be a list of T lists. Each list should be 13 length representing pressures 0 - 12, and T lists representing number of temperatures considered
    
    #this function does not use the colorbar because there are <5 unique configuration names.
    
    data_heatmap = np.array(config_data[::-1]) #invert due to heatmap plotting style of matplotlib
    
    fig, ax = plt.subplots(figsize=(15,15))

    heatmap = sns.heatmap(data=data_heatmap,linecolor = 'black', linewidths=1, cmap='plasma',annot=True,fmt='.3f',cbar=False, square=True,ax=ax)

    #Custom colour legend settings (hardcoded for now)
    legend = plot_colour_legend(config_data)
    
    plt.gca().add_artist(legend)

    #x and y labels/ticks & title settings
    ax.set_xlabel("Natural Log of Pressure Ratio of CO2/CO")
    ax.set_xticks(ax.get_xticks(),labels=range(0,13,1))
    ax.set_ylabel("Temperature (K)")
    ax.set_yticks(ax.get_yticks(),labels=tempture_list[::-1])
    ax.set_title("O* coverage concentration over T and P")

    fig.tight_layout()
    plt.show()