import os
import pandas as pd
import joblib
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

# Load model and scaler
model = joblib.load(os.path.join(os.path.dirname(__file__), '..', 'workforce_optimization_model3.pkl'))
scaler = joblib.load(os.path.join(os.path.dirname(__file__), '..', 'scaler3.pkl'))

# Load the dataset
df = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'employee_profile.csv'))

# Reapply feature engineering
df['Workload'] = df['NumberOfProject'] * df['AverageMonthlyHours']
df['PerformanceTrend'] = df['HistoricalPerformanceData'].apply(lambda x: [int(i) for i in x.split(', ')])
df['PerformanceTrend'] = df['PerformanceTrend'].apply(lambda x: pd.Series(x).diff().mean() if len(x) > 1 else 0)
df['Overtime'] = df['Overtime'].astype(int)
df['PromotionLast5Years'] = df['PromotionLast5Years'].astype(int)
df['Availability'] = df['Availability'].map({'Available': 1, 'Occupied': 0})

# Define the correct features that were used during scaler fitting
original_features = ['Workload', 'PerformanceTrend', 'BurnRate', 'Overtime', 'PromotionLast5Years', 'Availability', 'YearsAtCompany']

# Apply the scaler to the original features
df_scaled = scaler.transform(df[original_features])
df['WorkBalancePred'] = model.predict(df_scaled)

# Map predictions back to labels
df['WorkBalancePred'] = df['WorkBalancePred'].map({0: 'Underutilized', 1: 'Balanced', 2: 'Overworked'})

# Initialize Dash app
#app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], server=False)  # server=False for embedding in Django
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], assets_url_path='/static')

# Define the layout of the dashboard
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Workforce Optimization Dashboard", className="text-center"), className="mb-4")
    ]),
    dbc.Row([
        dbc.Col([
            html.Label("Role"),
            dcc.Dropdown(
                id='role-filter',
                options=[{'label': role, 'value': role} for role in df['Roles'].unique()],
                value=None,
                multi=True,
                placeholder="Select role(s)"
            ),
        ], width=4),
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(id='workload-distribution-chart'), width=6),
        dbc.Col(dcc.Graph(id='performance-trend-chart'), width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='workbalance-heatmap'), width=12)
    ]),
], fluid=True)

# Define callbacks for interactivity
@app.callback(
    Output('workload-distribution-chart', 'figure'),
    Output('performance-trend-chart', 'figure'),
    Output('workbalance-heatmap', 'figure'),
    Input('role-filter', 'value')
)
def update_charts(selected_roles):
    filtered_df = df.copy()
    
    if selected_roles:
        filtered_df = filtered_df[filtered_df['Roles'].isin(selected_roles)]
    
    # Workload Distribution Bar Chart
    workload_fig = px.bar(
        filtered_df,
        x='Roles',
        y='Workload',
        color='WorkBalancePred',
        barmode='group',
        title="Workload Distribution by Role"
    )

    # Performance Trend Line Chart
    performance_fig = px.line(
        filtered_df,
        x='YearsAtCompany',
        y='PerformanceTrend',
        color='WorkBalancePred',
        title="Performance Trend by Work Balance Prediction"
    )

    # Work Balance Heatmap
    heatmap_fig = px.density_heatmap(
        filtered_df,
        x='Roles',
        y='YearsAtCompany',
        z='Workload',
        title="Work Balance Heatmap"
    )
    
    return workload_fig, performance_fig, heatmap_fig

# If running this as a standalone Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
