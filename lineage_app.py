import dash
from dash import dcc, html, Input, Output, State
import dash_cytoscape as cyto
import networkx as nx
import random
import json # Needed for storing graph data

# --- Data Definition ---
# item: [list of components/origins]
dataset1 = {
    'Metal Tube': ['Melted Ore'],
    'Melted Ore': ['Ore'],
    'Ore': ['Mountain'],
    'Plastic Casing': ['Refined Oil'],
    'Refined Oil': ['Crude Oil'],
    'Crude Oil': ['Organic Deposits'],
    'Widget': ['Metal Tube', 'Plastic Casing', 'Software Module'],
    'Mountain': ['Tectonic Plates Impact'],
    'Tectonic Plates Impact': ['Tectonic Plates'],
    'Tectonic Plates': ['Cooled Magma'],
    'Cooled Magma': ['Magma'],
    'Organic Deposits': ['Ancient Life'],
    'Software Module': ['Code Library A', 'Code Library B'],
    'Code Library A': ['Algorithm X'],
    'Code Library B': ['Algorithm Y', 'Algorithm Z'],
    'Algorithm X': ['Mathematical Concept 1'],
    'Algorithm Y': ['Mathematical Concept 1'],
    'Algorithm Z': ['Mathematical Concept 2'],
    'Ancient Life': ['Early Earth Conditions'],
    'Magma': ['Early Earth Conditions'],
    'Early Earth Conditions': ['Planetary Formation'],
    'Mathematical Concept 1': ['Axioms Set 1'],
    'Mathematical Concept 2': ['Axioms Set 2'],
    'Planetary Formation': [],
    'Axioms Set 1': [],
    'Axioms Set 2': []
}

dataset2 = {
    'Book': ['Printed Pages', 'Cover'],
    'Printed Pages': ['Paper', 'Ink'],
    'Cover': ['Cardboard', 'Ink'],
    'Paper': ['Wood Pulp'],
    'Ink': ['Pigment', 'Binder'],
    'Cardboard': ['Wood Pulp'],
    'Wood Pulp': ['Tree'],
    'Pigment': ['Chemical Compound A'],
    'Binder': ['Chemical Compound B'],
    'Tree': ['Seed', 'Soil', 'Sunlight'],
    'Chemical Compound A': ['Raw Material X'],
    'Chemical Compound B': ['Raw Material Y'],
    'Seed': [],
    'Soil': [],
    'Sunlight': [],
    'Raw Material X': [],
    'Raw Material Y': []
}

datasets = {
    'Manufacturing Example': dataset1,
    'Book Example': dataset2
}
default_dataset_name = list(datasets.keys())[0]

# --- Helper Functions ---
def create_graph(lineage_data):
    G = nx.DiGraph()
    nodes = set()
    edges = []
    for child, parents in lineage_data.items():
        nodes.add(child)
        if not parents:
            nodes.add(child) # Ensure root nodes are added
        else:
            for parent in parents:
                nodes.add(parent)
                edges.append((parent, child))
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G

def create_cyto_elements(G):
    cyto_elements = []
    for node in G.nodes():
        cyto_elements.append({'data': {'id': node, 'label': node}})
    for edge in G.edges():
        cyto_elements.append({'data': {'source': edge[0], 'target': edge[1]}})
    return cyto_elements

# --- Default Stylesheet (Unchanged) ---
default_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#66c2a5',
            'label': 'data(label)',
            'width': 'mapData(id, 0, 100, 20, 60)',
            'height': 'mapData(id, 0, 100, 20, 60)',
            'font-size': '10px',
            'text-valign': 'center',
            'text-halign': 'center',
            'color': '#ffffff',
            'text-outline-width': 1,
            'text-outline-color': '#333333'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'line-color': '#cccccc',
            'width': 1,
            'curve-style': 'bezier',
            'target-arrow-shape': 'triangle',
            'target-arrow-color': '#cccccc'
        }
    },
    {
        'selector': '.highlighted_node',
        'style': {
            'background-color': '#fc8d62',
            'color': '#000000',
            'text-outline-color': '#ffffff',
             'border-width': 2,
             'border-color': '#e78ac3',
             'z-index': 9999
        }
    },
        {
        'selector': '.highlighted_ancestor',
        'style': {
            'background-color': '#8da0cb',
            'color': '#000000',
            'text-outline-color': '#ffffff',
             'border-width': 2,
             'border-color': '#a6d854',
             'z-index': 9998
        }
    },
    {
        'selector': '.highlighted_edge',
        'style': {
            'line-color': '#fc8d62',
            'target-arrow-color': '#fc8d62',
            'width': 2,
            'z-index': 9997
        }
    }
]


# --- Dash App Layout ---
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Information Origin Visualizer", style={'textAlign': 'center'}),
    html.Div([
        html.Label("Select Dataset:", style={'margin-right': '10px'}),
        dcc.Dropdown(
            id='dataset-dropdown',
            options=[{'label': name, 'value': name} for name in datasets.keys()],
            value=default_dataset_name, # Default value
            clearable=False,
            style={'width': '300px', 'display': 'inline-block'}
        )
    ], style={'textAlign': 'center', 'margin-bottom': '20px'}),

    html.P("Click on a node to see its origins (ancestors).", style={'textAlign': 'center'}),
    dcc.Store(id='graph-data-store'), # To store current graph data
    cyto.Cytoscape(
        id='cytoscape-lineage',
        # elements are now set by callback
        stylesheet=default_stylesheet,
        style={'width': '100%', 'height': '70vh'}, # Adjusted height slightly
        layout={
            'name': 'cose',
            'animate': True,
            'animationDuration': 500,
            'spacingFactor': 1.2,
            'nodeDimensionsIncludeLabels': True,
            'rankDir': 'TB',
            # 'roots' will be dynamically set if needed, or let cose handle it
        }
    )
])

# --- Callback to Update Graph Display based on Dropdown ---
@app.callback(
    Output('cytoscape-lineage', 'elements'),
    Output('graph-data-store', 'data'),
    Input('dataset-dropdown', 'value')
)
def update_graph_display(selected_dataset_name):
    lineage_data = datasets[selected_dataset_name]
    G = create_graph(lineage_data)
    cyto_elements = create_cyto_elements(G)
    graph_data_serializable = nx.node_link_data(G) # Store graph structure
    return cyto_elements, graph_data_serializable

# --- Callback for Interactivity (Highlighting) ---
@app.callback(
    Output('cytoscape-lineage', 'stylesheet'),
    Input('cytoscape-lineage', 'tapNodeData'),
    State('graph-data-store', 'data'), # Get current graph data from store
    State('cytoscape-lineage', 'stylesheet') # Keep existing stylesheet logic
)
def highlight_ancestors(node_data, graph_data_serializable, current_stylesheet):
    # Use default stylesheet as base, remove old highlights
    active_stylesheet = [s for s in default_stylesheet if not s['selector'].startswith('.highlighted')]

    if node_data is None or graph_data_serializable is None:
        return default_stylesheet # Return to default if no node clicked or graph not loaded

    # Rebuild graph from stored data
    G = nx.node_link_graph(graph_data_serializable)

    clicked_node_id = node_data['id']

    # Ensure the clicked node actually exists in the current graph
    if clicked_node_id not in G:
        return default_stylesheet # Should not happen, but safety check

    ancestors = nx.ancestors(G, clicked_node_id)
    nodes_to_highlight = ancestors.union({clicked_node_id})

    # Apply highlighting styles
    active_stylesheet.append({
        'selector': f'node[id = "{clicked_node_id}"]',
        'style': {
            'background-color': '#fc8d62',
            'color': '#000000',
            'text-outline-color': '#ffffff',
            'border-width': 3,
            'border-color': '#e78ac3',
            'z-index': 9999
        }
    })

    for ancestor_id in ancestors:
         active_stylesheet.append({
            'selector': f'node[id = "{ancestor_id}"]',
            'style': {
                'background-color': '#8da0cb',
                'color': '#000000',
                'text-outline-color': '#ffffff',
                'border-width': 2,
                'border-color': '#a6d854',
                'z-index': 9998
            }
        })

    edges_to_highlight = set()
    for u, v in G.edges():
        # Highlight edges connecting any two highlighted nodes
        if u in nodes_to_highlight and v in nodes_to_highlight:
             edges_to_highlight.add((u,v))

    for u, v in edges_to_highlight:
         active_stylesheet.append({
            'selector': f'edge[source = "{u}"][target = "{v}"]',
            'style': {
                 'line-color': '#fc8d62',
                 'target-arrow-color': '#fc8d62',
                 'width': 2,
                 'z-index': 9997
            }
         })

    return active_stylesheet

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True)

