import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import StrMethodFormatter
import matplotlib.ticker
from matplotlib.patches import Rectangle
import seaborn as sns
from heatmap_plot_funcs import heatmap_plot_legendonly

if __name__ == '__main__':
    start_temp = int(input("What is the starting temp (in Kelvins): "))
    end_temp = int(input("What is the ending temp (in Kelvins): "))
    step_size = int(input("What is the stepsize between T values: "))
    interval_size = (end_temp - start_temp)/step_size + 1

#Constant parameters
ZPE_oads = 0.085 # ZPE for adsorbate O*
n_TiC_bulkTiC = -56991.9 #eV

Slabenergy = pd.read_csv("Omega_TiC_V2.csv", usecols=["Slab_energy"])
nOads_origin = pd.read_csv("Omega_TiC_V2.csv", usecols=["n_Oads"])
Configs = pd.read_csv("Omega_TiC_V2.csv") #4083 x 1 

A1 = (nOads_origin*ZPE_oads - n_TiC_bulkTiC)

#addition of 3 terms in omega term.
A = np.add(A1,np.array(Slabenergy)) #4083 x 1 matrix

#Tx = np.linspace(500,1000, 6)
Tx = np.linspace(int(start_temp),int(end_temp),int(interval_size))
P = np.logspace(0, 12, 13)

config_name_list = [] #initialise list to store all config names, for T = 500 - 1000K.
all_indexes = [] #master list containing all indexes. 1 list == all min omegas for 1 unique T.

for T in np.arange(start_temp,end_temp+step_size,step_size): #np.arange function final value 1100 is not included, will stop at T=1000.

    #P = np.logspace(0, 12, 13)
    S_oads = 2.464*10**-4 #Entropy of adsorbate O*
    
    miuO = -437.465 + 0.096 - T*0.002317 + 0.00008617*T*(np.log(P))
    miuO = np.reshape(miuO,(1,13))

    nOads = np.tile(nOads_origin,13) # This is 4083 x 13 matrix, by repeating n0ads_origin 13 times horizontally.
    B1 = -(nOads*S_oads)*(T) #This is 4083 x 13
    B2 = -nOads_origin.dot(miuO) # This is 4083 x 13, created by matrix multiplication (4083,1) * (1,13)
    
    B = np.add(B1,B2)
    
    Ao = np.tile(A,13)# This is to convert 4083x1 to 4083x13, by repeating A 13 times horizontally.
    Omega = np.add(Ao,B) #4083 x 13 matrix. 4083 configs, 13 different pressure ranges. Complete result of all omegas.
    Omega = np.asarray(Omega,dtype=np.float64)
    
    #use indexing method to find config names,because row indexes are unique.
    #finds the minimum value in each column (pressure range) and stores index of particular row.
    #There should only be 78 config names, in a 6x13 matrix.
    minomega_indexes = {} #stores indexes of min omegas to obtain config names later. Renews for each T.
    
    new_df = pd.DataFrame(Omega,columns=np.linspace(0,12,13)) #converts Omega to pandas dataframe
    for col_name in new_df.columns:
        x = new_df[col_name].min() #find the minimum value of each column, corresponding to a range of P
        row_idx = new_df[new_df[col_name] == x].index.tolist() #get the row index of the min value
        minomega_indexes[col_name] = row_idx #collect the index here, total 13 indexes for 13 P ranges at each T.
        
    all_indexes.append(minomega_indexes) #collate indexes into a master list. This is done so 1 list = 1 unique temperature value T, containing 13 min omega values for 13 P ranges considered.

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
    heatmap_plot_legendonly(config_name_list,Tx)   
