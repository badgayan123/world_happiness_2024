from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px

# Load the happiness data
happiness = pd.read_csv('world_happiness.csv')

# Initialize the Dash app
app = Dash()

# Define the layout of the dashboard
app.layout = html.Div(style={'margin': '20px'}, children=[
    html.H1('World Happiness Dashboard'),
    html.P([
        'This dashboard shows the happiness score.',
        html.Br(),
        html.A('World Happiness Report Data Source',
               href='https://worldhappiness.report/',
               target='_blank')
    ]),

    # Region selection
    html.Div([
        html.Label('Select Region:'),
        dcc.RadioItems(
            id='region-radio',
            options=[{'label': region, 'value': region} for region in happiness['region'].unique()],
            value='North America',
            inline=True  # Display options inline
        ),
    ], style={'margin-bottom': '20px'}),

    # Country selection
    html.Div([
        html.Label('Select Country:'),
        dcc.Dropdown(
            id='country-dropdown',
            options=[],
            value='',  # Initially no country selected
            placeholder='Select a country'
        ),
    ], style={'margin-bottom': '20px'}),

    # Data type selection
    html.Div([
        html.Label('Select Data Type:'),
        dcc.RadioItems(
            id='data-radio',
            options=[
                {'label': 'Happiness Score', 'value': 'happiness_score'},
                {'label': 'Happiness Rank', 'value': 'happiness_rank'}
            ],
            value='happiness_score',
            inline=True  # Display options inline
        ),
    ], style={'margin-bottom': '20px'}),

    # Button to update output
    html.Button(id='submit-button', n_clicks=0, children='Update the Output'),

    # Graph for happiness data
    dcc.Graph(id='happiness-graph'),

    # Average display
    html.Div(id='average-div')
])


# Callback to update the country dropdown based on selected region
@app.callback(
    Output('country-dropdown', 'options'),
    Output('country-dropdown', 'value'),
    Input('region-radio', 'value')
)
def update_dropdown(selected_region):
    filtered_happiness = happiness[happiness['region'] == selected_region]
    country_options = [{'label': country, 'value': country} for country in filtered_happiness['country'].unique()]
    return country_options, country_options[0]['value'] if country_options else None


# Callback to update the graph and average display based on selected country and data type
@app.callback(
    Output('happiness-graph', 'figure'),
    Output('average-div', 'children'),
    Input('submit-button', 'n_clicks'),
    State('country-dropdown', 'value'),
    State('data-radio', 'value')
)
def update_graph(button_click, selected_country, selected_data):
    if not selected_country:
        return {}, "Please select a country."

    filtered_happiness = happiness[happiness['country'] == selected_country]

    if filtered_happiness.empty:
        return {}, f"No data available for {selected_country}."

    line_fig = px.line(
        filtered_happiness,
        x='year',
        y=selected_data,
        title=f'{selected_data.replace("_", " ").title()} in {selected_country}'
    )

    selected_avg = filtered_happiness[selected_data].mean()
    return line_fig, f'The average {selected_data.replace("_", " ")} for {selected_country} is {selected_avg:.2f}'


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

