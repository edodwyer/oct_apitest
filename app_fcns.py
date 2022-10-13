import datetime as dt
import pandas as pd
from user_inputs import import_user_inputs
from read_from_rds import get_sql_dat
import CallAPI as ca
import RunSim as rs

#%%

def get_params(user_params):
    
    dStart = user_params['dStart']
    Bat_capacity = user_params['Bat_capacity']
    ch_max = user_params['ch_max']
    Eff = user_params['Eff']
    agile_version = user_params['agile_version']
    
    numdays = 7 # Number of days to query
    dsmp = 30 # Sample time (minutes)
    
    
    dStart = dt.datetime.strptime(dStart, '%d-%b-%Y %H:%M')
    dEnd = dStart+dt.timedelta(1+numdays)
    
    dStart = dStart.isoformat()+'Z'
    dEnd = dEnd.isoformat()+'Z'
    
    samp = str(dsmp)+'min'
    ts = dsmp*60
    
    params = dict()
    params['dStart']=dStart
    params['dEnd']=dEnd
    params['samp']=samp
    params['agile_version']=agile_version
    params['ts'] = ts
    
    
    batparams = dict()
    batparams['BCAP'] = Bat_capacity*3600
    batparams['ch_max'] = ch_max
    batparams['Eff'] = Eff
    
    tindex=pd.date_range(dStart, dEnd, freq=samp, inclusive="left")
    
    return params, batparams, tindex

#%% Get tariffs

def get_tariffs(params):
    
    tariffs = dict()
    
    use_tar=params['agile_version']
    tariffs['Agile'] = ca.get_tar(use_tar,params['dStart'],params['dEnd']).resample(params['samp']).first().fillna(method="ffill")
    
    use_tar=3
    tariffs['Fixed'] = ca.get_tar(use_tar,params['dStart'],params['dEnd']).resample(params['samp']).first().fillna(method="ffill")
    
    return tariffs

#%% Get demand data

def get_demand(params):
    
    dem0 = get_sql_dat(params['dStart'],params['dEnd'])
    dem_df_full = dem0.tz_localize(tz='UTC')#[params['dStart']:params['dEnd']]
    dem_df = dem_df_full['elec_demand_W'].resample(params['samp']).mean()
    
    return dem_df

#%% Run simulation once

def run_1_sim(params,batparams,tariffs,dem_df,tindex,ch_start_hour=3,dch_start_hour=14):
    
    ch_start0 = dt.time(ch_start_hour)
    dch_start0 = dt.time(dch_start_hour)

    res_df,cost_df = rs.simcost(tindex,params['ts'],ch_start0,dch_start0,dem_df,batparams,tariffs)
    
    return res_df, cost_df

#%% Find best battery strategy

def run_best_sim(params,batparams,tariffs,dem_df,tindex):
    
    best_dch_start = dt.time(0)
    best_ch_start = dt.time(0)
    
    solsave = pd.DataFrame(index=[str(x)+":00" for x in range(21)],columns=[str(x)+":00" for x in range(16)])
    
    bestsol = 1e10
    
    for jj in range(0,16):
    
        for ii in range(jj,21):
        
            ch_start = dt.time(jj)
            dch_start = dt.time(ii)
            
            res_df0,cost_df0 = rs.simcost(tindex,params['ts'],ch_start,dch_start,dem_df,batparams,tariffs)
            
            solsave[str(jj)+":00"][str(ii)+":00"] = cost_df0.Agile.sum()
            
            if cost_df0.Agile.sum()<bestsol:
            
                cost_df = cost_df0
                res_df = res_df0
                
                bestsol = cost_df0.Agile.sum()
                best_dch_start = dch_start
                best_ch_start = ch_start
    
    return res_df, cost_df, bestsol, best_dch_start, best_ch_start
