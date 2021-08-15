import requests
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go

year=2021

pd.options.display.float_format = '{:,.2f}'.format

agency_req = requests.get('https://api.usaspending.gov/api/v2/references/toptier_agencies')
agency_json = agency_req.json()['results']
df = pd.DataFrame.from_dict(agency_json)

agency_ids = df['agency_id'].to_list()
agency_names = df['agency_name'].to_list()

data = []
for agency,agency_name in zip(agency_ids,agency_names):
    request = requests.get('https://api.usaspending.gov/api/v2/federal_obligations/?fiscal_year='+str(year)+'&funding_agency_id='+str(agency)+'&limit=500&page=1')
    req_json = request.json()['results']
    for element in req_json:
        element['agency_id'] = agency
        element['agency_name'] = agency_name
        data.append(element)

output = pd.DataFrame.from_dict(data)
output.obligated_amount = output.obligated_amount.astype(float)

output['budget'] = 'Budget'
fig = px.treemap(output, path=['budget', 'agency_name', 'account_title'], values='obligated_amount')
fig.data[0].textinfo = 'label+percent parent+percent root'
fig.data[0].hovertemplate='<b>%{label} </b> <br> Budget: $%{value:,.2f}<br> Percent Parent: %{percentParent:.2%}'

fig.data[0].outsidetextfont={'size':20}
fig.data[0].insidetextfont={'size':30}

fig.update_traces(hoverlabel_font_size=30, selector=dict(type='treemap'))

fig.update_traces(pathbar_thickness=50, selector=dict(type='treemap'))
fig.data[0].pathbar={'textfont':{'size':30}}

fig.update_layout(margin = dict(t=50, l=0, r=0, b=0))
fig.update_layout(paper_bgcolor='#f8f8f8', plot_bgcolor='#f8f8f8')


import dash
import dash_core_components as dcc
import dash_html_components as html

# create dash app and add treemap
app = dash.Dash(__name__, title='USA Budgets in '+str(year), meta_tags=[{'name': 'description', 'content': 'Mobile-friendly treemap visualization of the current US Budget'},{'name': 'keywords', 'content': 'css, python, heroku, flask, plotly, pandas, python3, dash, treemap, heroku-app, plotly-dash, plotly-python, plotly-express, spending, spend-analysis, us-data'},{'name': 'author', 'content': 'Siddharth Mathur'},{'name': 'robots', 'content': 'index, follow'}])
server = app.server
app.layout = html.Div([
    dcc.Graph(figure=fig, style={'height': '90vh'}, config= {'displaylogo': False})
])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8000)