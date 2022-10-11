#%% REQUEST PRICE DATA

def get_tar(use_tar,dStart,dEnd):
    '''
    Parameters
    ----------
    use_tar : Which tariff? Options: 0-> AGILE-18-02-21, 1->AGILE-22-07-22, 2->AGILE-22-08-31, 3->VAR-19-04-12.
    dStart : Start date.
    dEnd : End date.

    Returns
    -------
    prices : Dataframe of prices for timperiod.
    '''
    tar_types = ['AGILE-18-02-21','AGILE-22-07-22','AGILE-22-08-31','VAR-19-04-12']
    
    url0 = 'https://api.octopus.energy/v1/'
    url1 = 'products/'+tar_types[use_tar]+'/'
    url2 = 'electricity-tariffs/E-1R-'+tar_types[use_tar]+'-C/standard-unit-rates/'
    url3 = '?period_from='
    url4 = dStart
    url5 = '&period_to='
    url6 = dEnd
    
    url = (url0+url1+url2+url3+url4+url5+url6)
    
    # Call URL:
    r = requests.get(url)
    output_dict = r.json()

    reslist = output_dict['results']
    # If results are on multiple pages
    k=0
    while output_dict['next']!=None and k<10:
        k+=1
        r = requests.get(output_dict['next'])
        output_dict = r.json()
        reslist = reslist+output_dict['results']
    
    
    # Extract results and put in dataframe
    valid_from = [x['valid_from'] for x in reslist]
    value_exc_vat = [x['value_exc_vat'] for x in reslist]
    prices = pd.Series(value_exc_vat, index=valid_from)
    prices.index=pd.to_datetime(prices.index)
    
    # Make timeseries out of fixed price
    if use_tar==3:
        prices=pd.Series(data=prices,index=pd.date_range(prices.index[-1], dEnd, freq='30min', closed="left")).fillna(method='ffill')[dStart:dEnd]
    
    return prices