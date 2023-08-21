import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import StrMethodFormatter
import matplotlib.ticker
import numpy.ma as ma
import pandas as pd
import seaborn as sns

#def func(x, pos):
#    return f"{x:.2f}"#.replace("0.", ".").replace("1.00", "")

#Constant parameters
ZPE_oads = 0.085 # ZPE for adsorbate O*
n_TiC_bulkTiC = -56991.9 #eV

Slabenergy = pd.read_csv("Omega_TiC_V2.csv", usecols=["Slab_energy"])
nOads_origin = pd.read_csv("Omega_TiC_V2.csv", usecols=["n_Oads"])
Configs = pd.read_csv("Omega_TiC_V2.csv") #4083 x 1 

A1 = (nOads_origin*ZPE_oads - n_TiC_bulkTiC)

#addition of 3 terms in omega term.
A = np.add(A1,np.array(Slabenergy)) #4083 x 1 matrix

Tx = np.linspace(500,1000, 6)
P = np.logspace(0, 12, 13)

stepsize =100

config_name_list = [] #initialise list to store all config names, for T = 500 - 1000K.
all_indexes = [] #master list containing all indexes. 1 list == all min omegas for 1 unique T.

for T in np.arange(500,1100,stepsize): #np.arange function final value 1100 is not included, will stop at T=1000.

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
    
    theOmega = np.min(Omega, axis=0) #collapses into a 1 x 13 matrix (minimum omega only at a specific T)

    #matrix_for_compare = np.append(Omega,Configs,axis=1) #4083 x 14 matrix. Additional last column = configuration names.

    #use indexing method to find config names,because row indexes are unique.
    #finds the minimum value in each column (pressure range) and stores index of particular row.
    #There should only be 78 config names, in a 6x13 matrix.
    minomega_indexes = [] #stores indexes of min omegas to obtain config names later. Renews for each T.
    
    new_df = pd.DataFrame(Omega,columns=np.logspace(0,12,13)) #converts Omega to pandas dataframe
    for col_name in new_df.columns:
        x = min(new_df[col_name]) #find the minimum value of each column, corresponding to a range of P
        row_idx = new_df[new_df[col_name] == x].index[0] #get the row index of the min value
        minomega_indexes.append(row_idx) #collect the index here, total 13 indexes for 13 P ranges at each T.
        
    all_indexes.append(minomega_indexes) #collate indexes into a master list. This is done so 1 list = 1 unique temperature value T, containing 13 min omega values for 13 P ranges considered.

    if 'theOmega2' not in locals():
        theOmega2 = theOmega
    else:
        theOmega2 = np.ma.row_stack((theOmega2, theOmega))

#convert index numbers into config names, as obtained in the original CSV.
for lst in all_indexes:
    temp_config_list = []
    for val in lst:
        temp_config_list.append(Configs["Config_Name"][val])
    config_name_list.append(temp_config_list)

#obtain the number of unique config names in list (to determine if we need a colourmap or just a legend)
unique_configs = len(set([item for sublist in config_name_list for item in sublist]))

## if unique configs <= 5, use legend. If >5, use colormap gradient to mark out configs.

#Begin the heat map plot after generating the 13 x 13 TvP matrix
config_name_list = np.array(config_name_list[::-1]) #invert due to heatmap plotting style of matplotlib

#Generate list of lists of colours if unique_configs <= 5
#color_lst_lessthan5 = []
#if unique_configs <= 5:
#    for sublst in config_name_list:
#        for val in sublst:
            
fig, ax = plt.subplots()

#defining the parameters required to show the colourbar on the plot
norm = matplotlib.colors.BoundaryNorm(np.linspace(-3.5,1.5,6),5,clip=True) #determines the size of colourbar
Ocoverage = [12.0, '10.14', '10.56', '8.464', '10.0'] #colourbar labels
fmt = matplotlib.ticker.FuncFormatter(lambda x, pos: Ocoverage[::-1][norm(x)]) #format tick labels on colourbar 

#im, cbar = heatmap(np.zeros(config_name_list.shape),Tx[::-1],range(0,13,1),ax=ax,cmap=mpl.colormaps["PiYG"].resampled(5),norm=norm,cbar_kw=dict(ticks=np.arange(-3,2),format=fmt),cbarlabel = "O* coverages")

#should only be required when unique config names >5. Will update in future editions
sns.heatmap(data=config_name_list,cmap=mpl.colormaps["crest"].resampled(5),norm=norm,annot=True,fmt='.3f',cbar_kws=dict(ticks=np.arange(-3,2),format=fmt),ax=ax)

ax.set_xlabel("Natural Log of Pressure Ratio of CO2/CO")
ax.set_xticks(ax.get_xticks(),labels=range(0,13,1))
ax.set_ylabel("Temperature (K)")
ax.set_yticks(ax.get_yticks(),labels=Tx[::-1])
ax.set_title("O* coverage concentration over T and P")

fig.tight_layout()
plt.show()