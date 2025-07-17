import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import networkx as nx

# Sample legal graph setup
G = nx.DiGraph()
events = [
    ("Voting Rights Act (1965)", 1),
    ("Mobile v. Bolden (1980)", -1),
    ("VRA Amendment (1982)", 1),
    ("Shelby County v. Holder (2013)", -1),
    ("Brnovich v. DNC (2021)", -1),
]
for event, direction in events:
    G.add_node(event, direction=direction)
edges = [
    ("Voting Rights Act (1965)", "Mobile v. Bolden (1980)"),
    ("Mobile v. Bolden (1980)", "VRA Amendment (1982)"),
    ("VRA Amendment (1982)", "Shelby County v. Holder (2013)"),
    ("Shelby County v. Holder (2013)", "Brnovich v. DNC (2021)")
]
G.add_edges_from(edges)

# Position graph nodes using spring layout
pos = nx.spring_layout(G, seed=42)

# Create edge coordinates
edge_x = []
edge_y = []
for src, dst in G.edges():
    x0, y0 = pos[src]
    x1, y1 = pos[dst]
    edge_x += [x0, x1, None]
    edge_y += [y0, y1, None]

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=1, color='#888'),
    hoverinfo='none',
    mode='lines'
)

# Create node coordinates and colors
node_x = []
node_y = []
node_color = []
node_text = []

for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    direction = G.nodes[node]['direction']
    color = 'green' if direction == 1 else 'red' if direction == -1 else 'gray'
    node_color.append(color)
    node_text.append(node)

node_trace = go.Scatter(
    x=node_x, y=node_y, text=node_text,
    mode='markers+text', textposition="bottom center",
    hoverinfo='text',
    marker=dict(
        showscale=False,
        color=node_color,
        size=20,
        line_width=2
    )
)

# Sample metrics data
df_metrics = pd.DataFrame({
    "Year": [1965, 1980, 1982, 2013, 2021],
    "Turnout Gap (%)": [20, 15, 12, 10, 13],
    "Strict ID Laws": [0, 1, 5, 22, 30]
})

# Initialize Dash app
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Voting Rights Pathway Dashboard", style={'textAlign': 'center'}),
    dcc.Graph(id='pathway-graph', figure={
        'data': [edge_trace, node_trace],
        'layout': go.Layout(
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False)
        )
    }),
    dcc.Graph(id='metrics-graph', figure={
        'data': [
            go.Scatter(x=df_metrics['Year'], y=df_metrics['Turnout Gap (%)'], name="Turnout Gap", mode='lines+markers'),
            go.Scatter(x=df_metrics['Year'], y=df_metrics['Strict ID Laws'], name="Strict ID Laws", mode='lines+markers')
        ],
        'layout': go.Layout(title="Voting Metrics Over Time", xaxis_title="Year")
    })
])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
