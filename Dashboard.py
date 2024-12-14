# Import necessary libraries
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

# Initialize the Dash app
app = dash.Dash(__name__)

# Sample Dataset
df = pd.DataFrame({
    "Category": ["A", "B", "C", "D", "E"],
    "Value": [20, 34, 55, 77, 90],
    "Growth": [5, 10, 15, 20, 25],
    "Year": [2020, 2021, 2022, 2023, 2024]
})

# Create visualizations using Plotly
bar_chart = px.bar(df, x="Category", y="Value", title="Category vs Value")
line_chart = px.line(df, x="Year", y="Growth", title="Growth Over Years")

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Data Science Dashboard"),
    html.Div([
        html.Div([
            html.H3("Bar Chart: Category vs Value"),
            dcc.Graph(id="bar-chart", figure=bar_chart)
        ], className="six columns"),
        html.Div([
            html.H3("Line Chart: Growth Over Years"),
            dcc.Graph(id="line-chart", figure=line_chart)
        ], className="six columns")
    ], className="row"),
    
    # Dropdown for selecting chart category
    html.Div([
        html.H3("Select Category for Bar Chart"),
        dcc.Dropdown(
            id="category-dropdown",
            options=[{"label": category, "value": category} for category in df["Category"]],
            value="A"
        ),
        dcc.Graph(id="category-bar-chart")
    ]),
    
    # Slider for adjusting year range in the line chart
    html.Div([
        html.H3("Select Year Range for Growth Chart"),
        dcc.RangeSlider(
            id="year-slider",
            min=2020,
            max=2024,
            step=1,
            marks={2020: '2020', 2021: '2021', 2022: '2022', 2023: '2023', 2024: '2024'},
            value=[2020, 2024]
        ),
        dcc.Graph(id="growth-range-chart")
    ])
])

# Callback to update the bar chart based on the dropdown
@app.callback(
    Output("category-bar-chart", "figure"),
    [Input("category-dropdown", "value")]
)
def update_bar_chart(selected_category):
    filtered_df = df[df["Category"] == selected_category]
    return px.bar(filtered_df, x="Category", y="Value", title=f"Value for Category {selected_category}")

# Callback to update the growth line chart based on the slider
@app.callback(
    Output("growth-range-chart", "figure"),
    [Input("year-slider", "value")]
)
def update_growth_chart(selected_year_range):
    filtered_df = df[(df["Year"] >= selected_year_range[0]) & (df["Year"] <= selected_year_range[1])]
    return px.line(filtered_df, x="Year", y="Growth", title="Growth Over Selected Years")

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
