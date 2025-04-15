# Information Lineage Visualizer

## Description

This is an interactive web application built with Python (using Dash and Dash Cytoscape) to visualize the origin or lineage of information, components, or concepts. Inspired by tracing materials back to their source (e.g., metal tube -> ore -> mountain -> tectonic plates), this tool allows you to represent hierarchical or dependency relationships as a directed graph. Users can interactively explore these relationships by clicking on elements to see their origins.

## Features

* **Interactive Graph Visualization:** Displays lineage data as a directed graph.
* **Dataset Selection:** Allows switching between multiple predefined datasets via a dropdown menu.
* **Ancestor Highlighting:** Click on any node (element) in the graph to highlight it and all its ancestors (its components and their origins).
* **Web-Based UI:** Accessible through a standard web browser.
* **Built with Python:** Uses Dash for the web framework, Dash Cytoscape for graph rendering, and NetworkX for graph manipulation.

## Installation

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate

    # For Windows
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install dash dash-cytoscape networkx
    ```

## Usage

1.  **Run the application:**
    ```bash
    python lineage_app.py
    ```

2.  **Access the application:** Open your web browser and navigate to the address provided in the terminal (usually `http://127.0.0.1:8050/`).

3.  **Interact with the visualization:**
    * Use the dropdown menu at the top to select the dataset you want to view.
    * Click on any node within the graph. The clicked node, its ancestors (origins), and the connecting edges will be highlighted.
    * Click the background of the graph area to reset the highlighting.

## Data Format

The lineage data is currently defined within the `lineage_app.py` script as Python dictionaries. Each dictionary represents a dataset.

The structure for defining relationships is:

```python
dataset_name = {
    'resulting_item': ['component_1', 'component_2', ...],
    'component_1': ['sub_component_A', ...],
    # ... and so on
    'root_element': [] # Elements with no origins have an empty list
}

