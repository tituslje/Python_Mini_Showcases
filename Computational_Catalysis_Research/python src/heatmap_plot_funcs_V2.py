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


def heatmap_plot_legendonly(config_data,tempture_list,interval_size_input):
    #input data, config_data should be a list of T lists. Each list should be 13 length representing pressures 0 - 12, and T lists representing number of temperatures considered
    
    #this function does not use the colorbar because there are <5 unique configuration names.
    
    #Axis analyzer: determine if the plot is too tall to plot properly on matplotlib.
    #calculate the number of points for T and P axis respectively.
    T_points = len(config_data)
    P_points = len(config_data[0])
    
    #whichever has more data points (T/P), that means the axis will be longer. In that case make the longer axis the x axis, adjust figure size accordingly.
    if T_points > P_points:
        data_heatmap = np.array(config_data).T[::-1] #invert due to heatmap plotting style of matplotlib
        
        fig, ax = plt.subplots(figsize = (T_points,P_points))

        sns.heatmap(data=data_heatmap,linecolor = 'black', linewidths=0.5, cmap='plasma',annot=True,fmt='',cbar=False, square=True,ax=ax)

        #Custom colour legend settings (hardcoded for now)
        #legend = plot_colour_legend(config_data)

        #plt.gca().add_artist(legend)
        
        #custom tick locations setter to avoid tick location errors. Variable name different to avoid confusion with other plot.
        origin_x_ticks_T = plt.gca().get_xticks()
        origin_y_ticks_P = plt.gca().get_yticks()
        custom_x_ticks_T = np.linspace(origin_x_ticks_T[0],origin_x_ticks_T[-1],T_points)
        custom_y_ticks_P = np.linspace(origin_y_ticks_P[0],origin_y_ticks_P[-1],P_points)
        
        #x and y labels/ticks & title settings
        ax.set_ylabel("Natural Log of Pressure Ratio of CO2/CO")
        ax.set_yticks(custom_y_ticks_P,labels=range(0,13,1)[::-1])
        ax.set_xlabel("Temperature (K)")
        ax.set_xticks(custom_x_ticks_T,labels=tempture_list)
        ax.set_title("O* coverage concentration over T and P")
        
    elif T_points <= P_points:
        data_heatmap = np.array(config_data)[::-1]

        fig, ax = plt.subplots(figsize=(P_points,T_points))

        sns.heatmap(data=data_heatmap,linecolor = 'black', linewidths=0.5, cmap='plasma',annot=True,fmt='',cbar=False, square=True,ax=ax)

        #Custom colour legend settings (hardcoded for now)
        #legend = plot_colour_legend(config_data)
        
        #plt.gca().add_artist(legend)

        #custom tick locations setter to avoid tick location errors
        origin_x_ticks = plt.gca().get_xticks()
        origin_y_ticks = plt.gca().get_yticks()
        custom_x_ticks = np.linspace(origin_x_ticks[0],origin_x_ticks[-1],P_points)
        custom_y_ticks = np.linspace(origin_y_ticks[0],origin_y_ticks[-1],T_points)
        
        #x and y labels/ticks & title settings
        ax.set_xlabel("Natural Log of Pressure Ratio of CO2/CO")
        ax.set_xticks(custom_x_ticks,labels=range(0,P_points,1))
        ax.set_ylabel("Temperature (K)")
        ax.set_yticks(custom_y_ticks,labels=tempture_list[::-1])
        ax.set_title("O* coverage concentration over T and P")
    
    
    plt.tight_layout()
    plt.show()