import pandas as pd
import boto3
import plotly.express as px
import plotly.graph_objects as go
import config

# fetch data
s3 = boto3.client('s3', aws_access_key_id=config.aws_key, aws_secret_access_key=config.aws_secret)
output_csv = s3.download_file('miniviz-bucket', 'us_budget.csv', 'us_budget.csv')
output = pd.read_csv("us_budget.csv")

# create treemap
fig = px.treemap(output, path=['budget', 'agency_name', 'account_title'], values='obligated_amount')
fig.data[0].textinfo = 'label+percent parent+percent root'
fig.data[0].hovertemplate='<b>%{label} </b> <br> Budget: $%{value:,.2f}<br> Percent Parent: %{percentParent:.2%}'

fig.data[0].outsidetextfont={'size':20}
fig.data[0].insidetextfont={'size':30}

fig.update_traces(hoverlabel_font_size=30, selector=dict(type='treemap'))

fig.update_traces(pathbar_thickness=50, selector=dict(type='treemap'))
fig.data[0].pathbar={'textfont':{'size':30}}

fig.update_layout(autosize=True)
fig.update_layout(margin = dict(t=50, l=0, r=0, b=0))
fig.update_layout(paper_bgcolor='#f8f8f8', plot_bgcolor='#f8f8f8')


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# create dash app
app = dash.Dash(__name__, title='USA Spending', meta_tags=[{'name': 'description', 'content': 'Mobile-friendly treemap visualization of the current US Budget'},{'name': 'keywords', 'content': 'css, python, heroku, flask, plotly, pandas, python3, dash, treemap, heroku-app, plotly-dash, plotly-python, plotly-express, spending, spend-analysis, us-data'},{'name': 'author', 'content': 'Siddharth Mathur'},{'name': 'robots', 'content': 'index, follow'}])
server = app.server
app.layout = html.Div([
    dcc.Graph(figure=fig, style={'height': '90vh'}, config= {'displaylogo': False, 'displayModeBar': False})
])

if __name__ == '__main__':
    app.run_server(debug=False)
