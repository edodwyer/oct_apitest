import datetime as dt
import pandas as pd
import pickle
import numpy as np
import app_fcns as fcns
from user_inputs import import_user_inputs
from dash import Dash, html, dcc
import plotly.express as px
from plotly.subplots import make_subplots


dStart,Bat_capacity,ch_max,Eff,agile_version = import_user_inputs()
user_params = dict()
user_params['dStart'] = dStart
user_params['Bat_capacity'] = Bat_capacity
user_params['ch_max'] = ch_max
user_params['Eff'] = Eff
user_params['agile_version'] = agile_version
params,batparams,tindex = fcns.get_params(user_params)


tariffs = fcns.get_tariffs(params)


dem_df =  fcns.get_demand(params)


res_df1, cost_df1 = fcns.run_1_sim(params,batparams,tariffs,dem_df,tindex,ch_start_hour=3,dch_start_hour=14)


res_df,cost_df,bestsol,best_dch_start,best_ch_start = fcns.run_best_sim(params,batparams,tariffs,dem_df,tindex)


app = Dash(__name__)

dfa = pd.concat([tariffs['Agile'],tariffs['Fixed']],axis=1)
dfa.columns=['Agile','Fixed']
dfa=dfa.melt(var_name='tariff', value_name='value', ignore_index=False)

df1 = cost_df.cumsum()

subfig = make_subplots(specs=[[{"secondary_y": True}]])

fig = px.line(res_df, x=res_df.index, y=["Baseline_Grid","Grid"],color_discrete_sequence=px.colors.qualitative.Vivid)
figa = px.line(dfa, x=dfa.index, y=["value"],color='tariff',line_dash_sequence=['dot'],width=10)

figa.update_traces(yaxis="y2")

subfig.add_traces(fig.data + figa.data)
subfig.layout.xaxis.title="Time"
subfig.layout.yaxis.title="Power Consumption"
subfig.layout.yaxis2.title="price p/kWh"
subfig.layout.yaxis2.showgrid=False


bars=pd.DataFrame(data=[df1.iloc[-1].values],columns=df1.columns,index=['Total cost']).T


figures = [
            px.line(df1, x=df1.index, y=["Agile","Fixed"], title="Test",color_discrete_sequence=px.colors.qualitative.Vivid),
            px.bar(bars)
    ]

fig1 = make_subplots(rows=1, cols=len(figures)) 
fig1.layout.yaxis.title="Accumulated cost £"

for i, figure in enumerate(figures):
    for trace in range(len(figure["data"])):
        fig1.append_trace(figure["data"][trace], row=1, col=i+1)




app.layout = html.Div(children=[
    html.Div([        
        html.H1(children='Grid demand'),

        html.Div(children='''
            With and without battery+Agile.
        '''),

        dcc.Graph(
            id='f1',
            figure=subfig
        ),
    ]),


    html.Div([
        html.Div([
            html.H1(children='Cumulative cost'),

            html.Div(children='''
                With and without battery+Agile.
            '''),

            dcc.Graph(
                id='f2',
                figure=fig1
            ),
        ]),
    ]),    
])


if __name__ == '__main__':
    app.run_server(debug=True)