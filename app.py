import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

import datetime as dt
from datetime import datetime

#----------------------- Sales Data Preparation -----------------------------#
global df
df = pd.read_csv("Financial_Sample.csv")

cols = ['Manufacturing Price', 'Sale Price', 'Gross Sales', 'Discounts', ' Sales', 'COGS', 'Profit']
df[cols] = df[cols].apply(lambda x: x.str.lstrip('-'))
df[cols] = df[cols].apply(lambda x: x.str.lstrip('$'))
df[cols] = df[cols].apply(lambda x: x.str.replace(',',""))
df[cols] = df[cols].astype(float)
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', utc=False)
df['Date'] = df['Date'].dt.normalize()
df = df.sort_values(by="Date")
# df.set_index('Date', inplace=True)
df['Year']=df['Year'].astype(str)
df['Dates'] = pd.to_datetime(df['Date']).astype(np.int64)
df['Date']=pd.to_datetime(df['Date']).apply(lambda x: x.date())
min_date=df['Dates'].unique()[0]
max_date=df['Dates'].unique()[-1]
d=dict(zip(df['Dates'], df['Date']))
di=dict([list(d.items())[0],list(d.items())[-1]])


#--------------------------- Dash App Creation -------------------------------#
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server


#--------------------------- App Layout Creation -----------------------------#
app.layout = html.Div(
    [
        html.Div([
            html.H1("Financial Sales Dashboard",
                    style={'text-align': 'center', 'backgroundColor': 'midnightblue',
                           'color': 'white'})
        ]),

        html.Div([
            dbc.Card([
                dbc.CardHeader("Sales KPI",style={'font-weight': 'bold','text-align': 'center'}),
                dbc.CardBody(dcc.Graph(id='sales-kpi',figure={}))
                    ],style={"margin-left": "15px",'width':'15rem','display': 'inline-block'},outline=True,color="success"),
            dbc.Card([
                dbc.CardHeader("Segment",style={'font-weight': 'bold','text-align': 'center'}),
                dbc.CardBody(dcc.Dropdown(id='my-dpdn', multi=True, value=None,
                         options=[{'label':x, 'value':x}
                                  for x in sorted(df['Segment'].unique())],
                         placeholder='Segment'
                         ))
                    ],style={"margin-left": "100px",'width':'30rem','display': 'inline-block'},outline=True,color="dark"),
            dbc.Card([
                dbc.CardHeader("Country",style={'font-weight': 'bold','text-align': 'center'}),
                dbc.CardBody(dcc.Dropdown(id='my-dpdn2', multi=True, value=None,
                         options=[{'label':x, 'value':x}
                                  for x in sorted(df['Country'].unique())],
                          placeholder='Country'
                         ))
                    ],style={"margin-left": "25px",'width':'30rem','display': 'inline-block'},outline=True,color="dark")
                ]),
        html.Div(style={"margin-top": "5px"}),
        html.Div([
            dbc.Card([
                dbc.CardHeader("Profit KPI",style={'font-weight': 'bold','text-align': 'center'}),
                dbc.CardBody(dcc.Graph(id='profit-kpi',figure={}))
                    ],style={"margin-left": "15px",'width':'15rem','display': 'inline-block'},outline=True,color="success"),
            dbc.Card([
                dbc.CardHeader("Product",style={'font-weight': 'bold','text-align': 'center'}),
                dbc.CardBody(dcc.Dropdown(id='my-dpdn3', multi=True, value=None,
                         options=[{'label':x, 'value':x}
                                  for x in sorted(df[' Product '].unique())],
                          placeholder='Product'
                         ))
                    ],style={"margin-left": "100px",'width':'30rem','display': 'inline-block'},outline=True,color="dark"),
            dbc.Card([
                dbc.CardHeader("Discount Brand",style={'font-weight': 'bold','text-align': 'center'}),
                dbc.CardBody(dcc.Dropdown(id='my-dpdn4', multi=True, value=None,
                         options=[{'label':x, 'value':x}
                                  for x in sorted(df[' Discount Band '].unique())],
                          placeholder='Discount Band'
                         ))
                    ],style={"margin-left": "25px",'width':'30rem','display': 'inline-block'},outline=True,color="dark")
                ]),
        html.Div(style={"margin-top": "5px"}),
        html.Div([
            dbc.Card([
                dbc.CardHeader("Units Sold KPI",style={'font-weight': 'bold','text-align': 'center'}),
                dbc.CardBody(dcc.Graph(id='units-sold-kpi',figure={}))
                    ],style={"margin-left": "15px",'width':'15rem','display': 'inline-block'},outline=True,color="success"),
        ]),
        html.Div(style={"margin-top": "5px"}),
        html.Div([
            dbc.Card([
                dbc.CardHeader("DMY",style={'font-weight': 'bold','text-align': 'center','text-decoration': 'underline'}),
                html.Div(style={"margin-top": "5px"}),
                dbc.Card([
                    dbc.CardHeader("Date",style={'font-weight': 'bold','text-align': 'center'}),
                    dbc.CardBody(dcc.RangeSlider(id='date-range',updatemode = 'mouseup',min=min_date,max=max_date,step=4,value=[min_date,max_date],marks=di))
                        ],style={"margin-left": "22px",'width':'12rem','display': 'inline-block'},outline=True,color="dark"),
                html.Div(style={"margin-top": "5px"}),
                dbc.Card([
                    dbc.CardHeader("Year",style={'font-weight': 'bold','text-align': 'center'}),
                    dbc.CardBody(dcc.Dropdown(id='my-dpdn5', multi=True, value=None,
                         options=[{'label':x, 'value':x}
                                  for x in sorted(df['Year'].unique())],
                          placeholder='Select Year'
                         ))
                        ],style={"margin-left": "22px",'width':'12rem','display': 'inline-block'},outline=True,color="dark"),
                html.Div(style={"margin-top": "5px"}),
                dbc.Card([
                    dbc.CardHeader("Month",style={'font-weight': 'bold','text-align': 'center'}),
                    dbc.CardBody(dcc.Dropdown(id='my-dpdn6', multi=True, value=None,
                         options=[{'label':x, 'value':x}
                                  for x in sorted(df[' Month Name '].unique())],
                          placeholder='Select Month'
                         ))
                        ],style={"margin-left": "22px",'width':'12rem','display': 'inline-block'},outline=True,color="dark"),
                html.Div(style={"margin-top": "5px"}),
                    ],style={"margin-left": "15px",'width':'15rem','display': 'inline-block'},outline=True,color="primary"),
            dbc.Card([dcc.Graph(id='my-hist',clear_on_unhover=True, figure={})],style={"margin-left": "100px",'width':'30rem','display': 'inline-block'},outline=True,color="dark"),
            dbc.Card([dcc.Graph(id='my-hist2',clear_on_unhover=True, figure={})],style={"margin-left": "25px",'width':'30rem','display': 'inline-block'},outline=True,color="dark")
        ])

    ]

)



# Callback section: connecting the components
# ************************************************************************
# Bar chart - Single
@app.callback(
    Output('my-hist', 'figure'),
    Input('my-dpdn', 'value'),
    Input('my-dpdn2', 'value'),
    Input('my-dpdn3', 'value'),
    Input('my-dpdn4', 'value'),
    Input('my-dpdn5', 'value'),
    Input('my-dpdn6', 'value'),
    Input('date-range','value'),
    Input('my-hist2','hoverData')
)
def update_graph(seg,con,prd,disc,year,month,date,hoverData):
    dff=df.copy()
    dates=[i for i in dff['Dates'].unique() if i >= date[0] and i <= date[-1]]
    if hoverData==None:
        selection = [seg, con, prd, disc, year, month, dates]
    else:
        hoveredData = [hoverData['points'][0]['x']]
        selection = [seg, con, prd, disc, year, month, dates,hoveredData]
    # selection = [seg,con,prd,disc,year,month,dates]
    updated_selection = [i for i in selection if i is not None]
    updated_selection = list(filter(None,updated_selection))
    print(updated_selection)
    if len(updated_selection)==0:
        data=dff
        fighist = px.histogram(data, x='Segment', y='Units Sold')

    elif seg==None and len(updated_selection)>0:
        d=dict([(j,i) for i in updated_selection for j in df.columns if set(i).issubset(set(df[j].unique()))])
        print(d)
        for key in d:
            dff = dff[dff[key].isin(d[key])]
        data =  dff
        fighist = px.histogram(data, x='Segment', y='Units Sold')

    else:
        d = dict([(j, i) for i in updated_selection for j in df.columns if set(i).issubset(set(df[j].unique()))])
        print(d)
        for key in d:
            dff = dff[dff[key].isin(d[key])]
        data = dff
        fighist = px.histogram(data, x='Segment', y='Units Sold')

    fighist.update_layout(
        title=dict(text='<b>Units Sold by Segment and Product</b>', font=dict(family='Arial', size=20, color='green')),
        title_x=0.5, clickmode='event+select',hovermode='closest')
    return fighist

@app.callback(
    Output('my-hist2', 'figure'),
    Input('my-dpdn', 'value'),
    Input('my-dpdn2', 'value'),
    Input('my-dpdn3', 'value'),
    Input('my-dpdn4', 'value'),
    Input('my-dpdn5', 'value'),
    Input('my-dpdn6', 'value'),
    Input('date-range','value'),
    Input('my-hist','hoverData')
)
def update_graph(seg,con,prd,disc,year,month,date,hoverData):
    dff=df.copy()
    dates=[i for i in dff['Dates'].unique() if i >= date[0] and i <= date[-1]]
    if hoverData==None:
        selection = [seg, con, prd, disc, year, month, dates]
    else:
        hoveredData = [hoverData['points'][0]['x']]
        selection = [seg, con, prd, disc, year, month, dates,hoveredData]
    # selection = [seg,con,prd,disc,year,month,dates]
    updated_selection = [i for i in selection if i is not None]
    updated_selection = list(filter(None,updated_selection))
    print(updated_selection)
    if len(updated_selection)==0:
        data=dff
        fighist = go.Figure(data=[go.Bar( name = 'Profit',  x = data['Segment'].unique(), y = data['Profit']), go.Bar( name = 'Sales', x = data['Segment'].unique(), y = data[' Sales'])])


    elif seg==None and len(updated_selection)>0:
        d=dict([(j,i) for i in updated_selection for j in df.columns if set(i).issubset(set(df[j].unique()))])
        for key in d:
            dff = dff[dff[key].isin(d[key])]
        data =  dff
        fighist = go.Figure(data=[go.Bar( name = 'Profit',  x = data['Segment'].unique(), y = data['Profit']), go.Bar( name = 'Sales', x = data['Segment'].unique(), y = data[' Sales'])])


    else:
        d = dict([(j, i) for i in updated_selection for j in df.columns if set(i).issubset(set(df[j].unique()))])
        for key in d:
            dff = dff[dff[key].isin(d[key])]
        data = dff
        fighist = go.Figure(data=[go.Bar( name = 'Profit',  x = data['Segment'].unique(), y = data['Profit']), go.Bar( name = 'Sales', x = data['Segment'].unique(), y = data[' Sales'])])

    fighist.update_layout(title=dict(text='<b>Sales and Profit by Segment and Product</b>',
                                     font=dict(family='Arial', size=20, color='green')), title_x=0.5,
                          clickmode='event+select',hovermode='closest')
    return fighist

# Sales KPI
@app.callback(
    Output('sales-kpi', 'figure'),
    Input('my-dpdn', 'value'),
    Input('my-dpdn2', 'value'),
    Input('my-dpdn3', 'value'),
    Input('my-dpdn4', 'value'),
    Input('my-dpdn5', 'value'),
    Input('my-dpdn6', 'value'),
    Input('date-range','value'),
    Input('my-hist','hoverData'),
    Input('my-hist2','hoverData')
)

def update_graph(seg,con,prd,disc,year,month,date,hist_hover,hist2_hover):
    dff = df.copy()
    dates = [i for i in dff['Dates'].unique() if i >= date[0] and i <= date[-1]]
    if hist_hover==None and hist2_hover==None:
        selection = [seg, con, prd, disc, year, month, dates]
    elif hist_hover!=None and hist2_hover==None:
        hist_hovered=[hist_hover['points'][0]['x']]
        selection = [seg, con, prd, disc, year, month, dates,hist_hovered]
    elif hist_hover==None and hist2_hover!=None:
        hist2_hovered = [hist2_hover['points'][0]['x']]
        selection = [seg, con, prd, disc, year, month, dates, hist2_hovered]
    # selection = [seg, con, prd, disc, year, month,dates]
    updated_selection = [i for i in selection if i is not None]
    updated_selection = list(filter(None, updated_selection))
    print(updated_selection)
    if len(updated_selection)==0:
        data=dff
        figkpi = go.Figure(data=[go.Indicator(value=data[' Sales'].sum(),number={"font":{"size":30}})])
    else:
        d = dict([(j, i) for i in updated_selection for j in df.columns if set(i).issubset(set(df[j].unique()))])
        for key in d:
            dff = dff[dff[key].isin(d[key])]
        data = dff
        figkpi = go.Figure(data=[go.Indicator(value=data[' Sales'].sum(),number={"font":{"size":30}})])
    figkpi.update_layout(height=30)
    return figkpi

# Profit KPI
@app.callback(
    Output('profit-kpi', 'figure'),
    Input('my-dpdn', 'value'),
    Input('my-dpdn2', 'value'),
    Input('my-dpdn3', 'value'),
    Input('my-dpdn4', 'value'),
    Input('my-dpdn5', 'value'),
    Input('my-dpdn6', 'value'),
    Input('date-range','value'),
    Input('my-hist','hoverData'),
    Input('my-hist2','hoverData')
)

def update_graph(seg,con,prd,disc,year,month,date,hist_hover,hist2_hover):
    dff = df.copy()
    dates = [i for i in dff['Dates'].unique() if i >= date[0] and i <= date[-1]]
    if hist_hover==None and hist2_hover==None:
        selection = [seg, con, prd, disc, year, month, dates]
    elif hist_hover!=None and hist2_hover==None:
        hist_hovered=[hist_hover['points'][0]['x']]
        selection = [seg, con, prd, disc, year, month, dates,hist_hovered]
    elif hist_hover==None and hist2_hover!=None:
        hist2_hovered = [hist2_hover['points'][0]['x']]
        selection = [seg, con, prd, disc, year, month, dates, hist2_hovered]
    # selection = [seg, con, prd, disc, year, month,dates]
    updated_selection = [i for i in selection if i is not None]
    updated_selection = list(filter(None, updated_selection))
    print(updated_selection)
    if len(updated_selection)==0:
        data=dff
        figkpi = go.Figure(data=[go.Indicator(value=data['Profit'].sum(),number={"font":{"size":30}})])
    else:
        d = dict([(j, i) for i in updated_selection for j in df.columns if set(i).issubset(set(df[j].unique()))])
        for key in d:
            dff = dff[dff[key].isin(d[key])]
        data = dff
        figkpi = go.Figure(data=[go.Indicator(value=data['Profit'].sum(),number={"font":{"size":30}})])
    figkpi.update_layout(height=30)
    return figkpi

# Units Sold KPI
@app.callback(
    Output('units-sold-kpi', 'figure'),
    Input('my-dpdn', 'value'),
    Input('my-dpdn2', 'value'),
    Input('my-dpdn3', 'value'),
    Input('my-dpdn4', 'value'),
    Input('my-dpdn5', 'value'),
    Input('my-dpdn6', 'value'),
    Input('date-range','value'),
    Input('my-hist','hoverData'),
    Input('my-hist2','hoverData')
)

def update_graph(seg,con,prd,disc,year,month,date,hist_hover,hist2_hover):
    dff = df.copy()
    dates = [i for i in dff['Dates'].unique() if i >= date[0] and i <= date[-1]]
    if hist_hover==None and hist2_hover==None:
        selection = [seg, con, prd, disc, year, month, dates]
    elif hist_hover!=None and hist2_hover==None:
        hist_hovered=[hist_hover['points'][0]['x']]
        selection = [seg, con, prd, disc, year, month, dates,hist_hovered]
    elif hist_hover==None and hist2_hover!=None:
        hist2_hovered = [hist2_hover['points'][0]['x']]
        selection = [seg, con, prd, disc, year, month, dates, hist2_hovered]
    # selection = [seg, con, prd, disc, year, month,dates]
    updated_selection = [i for i in selection if i is not None]
    updated_selection = list(filter(None, updated_selection))
    print(updated_selection)
    if len(updated_selection)==0:
        data=dff
        figkpi = go.Figure(data=[go.Indicator(value=data['Units Sold'].sum(),number={"font":{"size":30}})])
    else:
        d = dict([(j, i) for i in updated_selection for j in df.columns if set(i).issubset(set(df[j].unique()))])
        for key in d:
            dff = dff[dff[key].isin(d[key])]
        data = dff
        figkpi = go.Figure(data=[go.Indicator(value=data['Units Sold'].sum(),number={"font":{"size":30}})])
    figkpi.update_layout(height=30)
    return figkpi


if __name__=='__main__':
    app.run_server(debug=True)
