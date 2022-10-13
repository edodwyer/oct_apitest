import datetime as dt

def import_user_inputs():
    
    dStart='29-Sep-2022 00:00'
    
    agile_version = 2
    
        
    
    # Battery parameters:
    
    Bat_capacity = 13 # Capacity of battery in kWh
    
    ch_max = 3 # Max charge/discharge power in kW
    
    Eff = 0.9 # Round-trip efficiency
    
        
    
    return dStart,Bat_capacity,ch_max,Eff,agile_version