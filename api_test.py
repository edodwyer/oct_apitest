import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import numpy as np
import CallAPI as ca
import RunSim as rs


dStart='29-Sep-2022 00:00'
numdays = 10 # Number of days to query
dsmp = 30 # Sample time (minutes)


dStart = dt.datetime.strptime(dStart, '%d-%b-%Y %H:%M')
dEnd = dStart+dt.timedelta(1+numdays)

dStart = dStart.isoformat()+'Z'
dEnd = dEnd.isoformat()+'Z'

samp = str(dsmp)+'min'
ts = dsmp*60

# Battery parameters:
Bat_capacity = 13 # Capacity of battery in kWh
ch_max = 1 # Max charge/discharge power in kW
Eff = 0.9 # Round-trip efficiency

#%% Get tariffs
# use_tar = 0 # Select from: 0-> AGILE-18-02-21, 1->AGILE-22-07-22, 2->AGILE-22-08-31, 3->VAR-19-04-12
tariffs = dict()

use_tar=2
tariffs['Agile'] = ca.get_tar(use_tar,dStart,dEnd).resample(samp).first().fillna(method="ffill")

use_tar=3
tariffs['Fixed'] = ca.get_tar(use_tar,dStart,dEnd).resample(samp).first().fillna(method="ffill")

#%% Get demand data

dem_df_full = pickle.load(open("synth_dem.p","rb")).tz_localize(tz='UTC')[dStart:dEnd]
dem_df = dem_df_full['elec_demand_W'].resample(samp).mean()

#%% Run simulation once
ch_start0 = dt.time(3)
dch_start0 = dt.time(14)

tindex=pd.date_range(dStart, dEnd, freq=samp, inclusive="left")

batparams = dict()
batparams['BCAP'] = Bat_capacity*3600
batparams['ch_max'] = ch_max
batparams['Eff'] = Eff

res_df,cost_df = rs.simcost(tindex,ts,ch_start0,dch_start0,dem_df,batparams,tariffs)

#%% Battery strategy search
 
best_dch_start = dt.time(0)
best_ch_start = dt.time(0)

solsave = pd.DataFrame(index=[str(x)+":00" for x in range(21)],columns=[str(x)+":00" for x in range(16)])

bestsol = 1e10
for jj in range(0,16):
    for ii in range(jj,21):
        ch_start = dt.time(jj)
        dch_start = dt.time(ii)
        res_df0,cost_df0 = rs.simcost(tindex,ts,ch_start,dch_start,dem_df,batparams,tariffs)
        solsave[str(jj)+":00"][str(ii)+":00"] = cost_df0.Agile.sum()
        
        if cost_df0.Agile.sum()<bestsol:
            cost_df = cost_df0
            res_df = res_df0
            bestsol = cost_df0.Agile.sum()
            best_dch_start = dch_start
            best_ch_start = ch_start


#%%
fig, ax1 = plt.subplots(figsize=(15, 6), dpi=300, edgecolor='k')
ax1.plot(res_df.Baseline_Grid)
ax1.plot(res_df.Grid)
# plt.plot(res_df.Charge*1000)
ax2=ax1.twinx()
ax2.plot(tariffs['Agile'],'k')
ax2.plot(tariffs['Fixed'],'k--')
#%%
fig = plt.figure(figsize=(15, 6), dpi=300)
cost_df.cumsum().plot(ax=plt.gca())
#%%
fig, ax = plt.subplots(figsize=(6, 6), dpi=300)
cost_df.cumsum().iloc[-1].plot.bar(ax=plt.gca())

