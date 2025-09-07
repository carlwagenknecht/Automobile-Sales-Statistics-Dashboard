import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv'
)

# Initialise app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    # Title
    html.H1(
        " Automobile Sales Statistics Dashboard",
        style={
            'textAlign': 'center',
            'color': '#003366',
            'fontFamily': 'Arial',
            'marginBottom': '30px'
        }
    ),

    # Dropdown for statistics type
    dcc.Dropdown(
        id='stats-dropdown',
        options=[
            {'label': 'Recession Statistics', 'value': 'Recession Statistics'},
            {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'}
        ],
        placeholder="Select statistics type"
    ),

    # Dropdown for year
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(y), 'value': y} for y in sorted(data['Year'].unique())],
        placeholder="Select a year"
    ),

    # Output charts
    html.Div(id='output-container')
])

# Callback
@app.callback(
    Output('output-container', 'children'),
    [Input('year-dropdown', 'value'),
     Input('stats-dropdown', 'value')]
)
def update_charts(input_year, selected_statistics):
    if selected_statistics == 'Recession Statistics':
        recession_data = data[data['Recession'] == 1]

        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales',
                           title="Average Automobile Sales During Recession")
        )

        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales',
                          title="Average Vehicles Sold by Type During Recession")
        )

        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
                          title="Total Advertising Expenditure Share by Vehicle Type During Recession")
        )

        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
                          labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                          title='Effect of Unemployment Rate on Vehicle Type and Sales')
        )

        return [
            html.Div([R_chart1, R_chart2], style={'display': 'flex'}),
            html.Div([R_chart3, R_chart4], style={'display': 'flex'})
        ]

    elif selected_statistics == 'Yearly Statistics' and input_year:
        yearly_data = data[data['Year'] == input_year]

        yas = yearly_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas, x='Year', y='Automobile_Sales',
                           title=f"Yearly Automobile Sales for {input_year}")
        )

        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mas, x='Month', y='Automobile_Sales',
                           title=f"Monthly Automobile Sales for {input_year}")
        )

        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales',
                          title=f"Average Vehicles Sold by Vehicle Type in {input_year}")
        )

        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type',
                          title=f"Total Advertising Expenditure for Each Vehicle in {input_year}")
        )

        return [
            html.Div([Y_chart1, Y_chart2], style={'display': 'flex'}),
            html.Div([Y_chart3, Y_chart4], style={'display': 'flex'})
        ]

    return html.Div("Select a statistics type and year to display charts.")


if __name__ == '__main__':
    app.run(debug=True)


