import pandas as pd
import numpy as np
#%%
def simcost(tindex,ts,ch_start,dch_start,dem_df,batparams,tar):
    '''
    Parameters
    ----------
    tindex : Time-series range.
    ch_start : Time of the day that battery charging period begins.
    dch_start : Time of the day that battery discharging period begins.
    dem_df : Electricity demand.
    batparams : Battery parameters.

    Returns
    -------
    res_df : Simulated grid consumption and battery usage data.
    cost_df : Simulated electricity costs.
    '''
    soc = 0
    gridpower=[]
    grid_baseline=[]
    ch_prof=[]
    dch_prof=[]
    soc_prof=[]
    agile_cost=[]
    fixed_cost=[]
    for ii in tindex:
        # In charging or discharging window:
        if ii.time()>ch_start and ii.time()<dch_start:
            ch=batparams['ch_max']
            dch=0
        else:
            ch=0
            dch=min(batparams['ch_max'],0.001*dem_df[ii])
        
        # Update state of charge:
        soc_ = soc
        soc = min(batparams['BCAP'],max(0,soc_+ts*(ch*batparams['Eff']-dch/batparams['Eff'])))
        dch = max(0,soc_-soc)/ts
        ch = max(0,soc-soc_)/ts
        
        # Calculate power from grid
        gpwr = 0.001*dem_df[ii]-dch+ch # Note the conversion from W to kW
        gpwr_nobat = 0.001*dem_df[ii]
        
        # Append new entries to arrays
        gridpower.append(max(0,gpwr))
        grid_baseline.append(max(0,gpwr_nobat))
        ch_prof.append(ch)
        dch_prof.append(dch)
        soc_prof.append(soc/batparams['BCAP'])
        agile_cost.append(max(0,gpwr)*tar['Agile'][ii]*(0.01/2))  # scaled by (0.01/2) to get to £ (demand is half-hourly W samples, tariff is in p/kWh)
        fixed_cost.append(max(0,gpwr_nobat)*tar['Fixed'][ii]*(0.01/2)) # scaled by (0.01/2) to get to £ (demand is half-hourly W samples, tariff is in p/kWh)
                
    res_df = pd.DataFrame(index=tindex,data=np.array([gridpower,grid_baseline,ch_prof,dch_prof,soc_prof]).T,columns=["Grid","Baseline_Grid","Charge","Discharge","SOC"])
    cost_df = pd.DataFrame(index=tindex,data=np.array([agile_cost,fixed_cost]).T,columns=["Agile","Fixed"])
    
    return res_df,cost_df
