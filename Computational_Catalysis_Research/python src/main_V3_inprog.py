import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import StrMethodFormatter
import matplotlib.ticker
from matplotlib.patches import Rectangle
import seaborn as sns
from heatmap_plot_funcs_V2 import heatmap_plot

if __name__ == '__main__':
    ##Key in variable temperature and pressure values, user inputs
    ##Currently, step sizes for pressure can only accept integer values due to range function used in generating the plots.
    ##
    # start and end temp/pres are self-explanatory;
    # step sizes are used to determine the spacing between data points, used in graphing function
    # interval sizes are used to generate the number of data points for the iterative calculation in the for loops below in this file. Particularly, it is used to generate the values in Tx and P vectors.
    
    start_temp = int(input("What is the starting temp (in Kelvins): "))
    end_temp = int(input("What is the ending temp (in Kelvins): "))
    step_size_T = float(input("What is the stepsize between T values: "))
    interval_size_T = int((end_temp - start_temp)/step_size_T + 1)
    ##################################Divider for clarity################################
    start_pres = int(input("What is the starting pressure (in integer, logspace): "))
    end_pres = int(input("What is the final pressure (in integer, logspace): "))
    step_size_P = float(input("What is the stepsize between T values: "))
    interval_size_P = int((end_pres - start_pres)/step_size_P + 1)

## Plot paramters in a list, to be passed into function for plotting ease of reference. 
temp_plot_params = [start_temp,end_temp,interval_size_T]
pres_plot_params = [start_pres,end_pres,interval_size_P]

#Constant parameters
ZPE_oads = 0.085 # ZPE for adsorbate O*
n_TiC_bulkTiC = -56991.9 #eV

Slabenergy = pd.read_csv("VC_111_withConfigs.csv", usecols=["Slab_energy"])
nOads_origin = pd.read_csv("VC_111_withConfigs.csv", usecols=["n_Oads"])
Configs = pd.read_csv("VC_111_withConfigs.csv") #4083 x 1 

A1 = (nOads_origin*ZPE_oads - n_TiC_bulkTiC)

#addition of 3 terms in omega term.
A = np.add(A1,np.array(Slabenergy)) #4083 x 1 matrix

Tx = np.linspace(start_temp ,end_temp ,interval_size_T)
P = np.logspace(start_pres, end_pres, interval_size_P)

config_name_list = [] #initialise list to store all config names, for user input temperature range.
all_indexes = [] #master list containing all indexes. 1 list == all min omegas for 1 unique T.

for T in np.arange(start_temp,end_temp+step_size_T,step_size_T): #np.arange function final value 1100 is not included, will stop at T=1000. Thus, the end_temp+step_size_T is needed to circumvent this.
    #stores indexes of min omegas to obtain config names later. Renews for each T. Final format is like this pressure1: [index1, index2,...] E.g. 1.0: [3028,3028,...],2.0:[...],...
    
    minomega_indexes = {} 
    
    #dictionary minomega_indexes empties itself for a new value of T after it's unique key-value pairs for a particular T are appended to the list all_indexes. 
    
    for pressure in P:
        S_oads = 2.464*10**-4 #Entropy of adsorbate O*
        
        
        miuO = -437.465 + 0.096 - T*0.002317 + 0.00008617*T*(np.log(pressure))
        #miuO = np.reshape(miuO,(1,1))
        
        B1 = -(nOads_origin*S_oads)*(T) #This is 4083 x 1
        B2 = -nOads_origin*miuO # This is 4083 x 1, created by matrix multiplication (4083,1) * (1,1)
        B = B1 + B2
        
        Omega = pd.DataFrame()
        Omega[pressure] = np.add(A,B) #4083 x 1 matrix. 4083 configs for a given pressure range. Complete result of all omegas for a particular T,P.

        #use indexing method to find config names,because row indexes are unique.
        #finds the minimum value in each column (pressure range) and stores index of particular row.
        #There should only be T*P config names, in a TxP matrix.
        
        x = Omega[pressure].min() #find the minimum value of each column, corresponding to a range of P
        row_idx = Omega[Omega[pressure] == x].index.tolist() #get the row index of the min value
        minomega_indexes[pressure] = row_idx #collect the index here, only 1 index at 1 T and 1 P.
    
    #collate indexes into a master list all_indexes for each T. This is done so 1 list = 1 unique temperature value T, containing P min omega values for P pressure ranges considered.
    
    all_indexes.append(minomega_indexes) 

#convert index numbers into config names, as obtained in the original CSV.
for dict in all_indexes:
    temp_config_list = []
    for key,lst in dict.items():
        if len(lst) > 1:
            temp_config_list.append(Configs["Config_Name"][lst[0:len(lst)+1]])
        else:
            temp_config_list.append(Configs["Config_Name"][lst[0]])
    config_name_list.append(temp_config_list)

#obtain the number of unique config names in list (to determine if we need a colourmap or just a legend)
unique_configs = len(set([item for sublist in config_name_list for item in sublist]))

## if unique configs <= 5, use legend. If >5, use colormap gradient to mark out configs.

if unique_configs <= 5:
    selected_colors = []
    heatmap_plot(config_name_list, temp_plot_params, pres_plot_params)   
elif unique_configs > 5:
    heatmap_plot(config_name_list, temp_plot_params, pres_plot_params,colorbar_option=True)