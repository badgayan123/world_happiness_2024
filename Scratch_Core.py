from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

# Load the data
happiness = pd.read_csv('world_happiness.csv')

# Create a line plot for the USA happiness score
line_fig = px.line(
    happiness[happiness['country'] == 'United States'],
    x='year',
    y='happiness_score',
    title='Happiness Score in the USA'
)

# Initialize the Dash app
app = Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1('World Happiness Dashboard'),
    html.P([
        'This dashboard shows the happiness score.',
        html.Br(),
        html.A(
            'World Happiness Report Data Source',
            href='https://worldhappiness.report/',
            target='_blank'
        )
    ]),

    # RadioItems with inline formatting for horizontal layout
    html.Label('Select Region (RadioItems):'),
    dcc.RadioItems(
        options=[{'label': region, 'value': region} for region in happiness['region'].unique()],
        value='North America',
        inline=True  # Display options in a single row
    ),

    # Checklist with inline formatting
    html.Label('Select Multiple Regions (Checklist):'),
    dcc.Checklist(
        options=[{'label': region, 'value': region} for region in happiness['region'].unique()],
        value=['North America'],
        inline=True  # Display options in a single row
    ),

    # Dropdown for countries
    dcc.Dropdown(
        options=[{'label': country, 'value': country} for country in happiness['country'].unique()],
        value='United States'
    ),

    # Graph for happiness score
    dcc.Graph(figure=line_fig)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
