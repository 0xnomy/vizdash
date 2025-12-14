"""
Graph Network Visualizations
Creates network visualizations using different layouts
"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
from pathlib import Path
import re

# Set up paths
BASE_PATH = Path(__file__).parent.parent
DATA_PATH = BASE_PATH / "datasets" / "graph"
OUTPUT_PATH = BASE_PATH / "outputs"
OUTPUT_PATH.mkdir(exist_ok=True)

def parse_pajek_net_file(filepath):
    """Parse Pajek .net file format"""
    print(f"Parsing {filepath.name}...")
    
    G = nx.Graph()
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    mode = None
    for line in lines:
        line = line.strip()
        
        if line.startswith('*Vertices'):
            mode = 'vertices'
            continue
        elif line.startswith('*Edges') or line.startswith('*Arcs'):
            mode = 'edges'
            continue
        
        if mode == 'vertices' and line:
            # Parse vertex: ID "Label" x y z
            parts = line.split()
            if len(parts) >= 2:
                node_id = int(parts[0])
                # Extract label from quotes if present
                label_match = re.search(r'"([^"]*)"', line)
                label = label_match.group(1) if label_match else parts[1]
                G.add_node(node_id, label=label)
        
        elif mode == 'edges' and line:
            # Parse edge: source target weight
            parts = line.split()
            if len(parts) >= 2:
                source = int(parts[0])
                target = int(parts[1])
                weight = float(parts[2]) if len(parts) > 2 else 1.0
                G.add_edge(source, target, weight=weight)
    
    print(f"Loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    return G

def load_graph_data(filename="Ring25.net"):
    """Load graph network dataset"""
    print(f"\nLoading graph data: {filename}")
    filepath = DATA_PATH / filename
    G = parse_pajek_net_file(filepath)
    return G

def visualize_spring_layout(G, output_file="graph_spring.png"):
    """Create spring (force-directed) layout visualization"""
    print("\nCreating spring layout visualization...")
    
    plt.figure(figsize=(14, 14))
    
    # Spring layout
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Calculate node properties
    degrees = dict(G.degree())
    node_sizes = [300 + degrees[node] * 100 for node in G.nodes()]
    node_colors = [degrees[node] for node in G.nodes()]
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, alpha=0.3, width=2, edge_color='#888888')
    
    # Draw nodes with color gradient based on degree
    nodes = nx.draw_networkx_nodes(G, pos,
                                   node_color=node_colors,
                                   node_size=node_sizes,
                                   cmap='viridis',
                                   alpha=0.9,
                                   edgecolors='black',
                                   linewidths=2)
    
    # Draw labels
    labels = nx.get_node_attributes(G, 'label')
    if not labels:
        labels = {node: str(node) for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
    
    # Add colorbar
    plt.colorbar(nodes, label='Node Degree', shrink=0.8)
    
    plt.title(f"Network Graph - Spring Layout\n{G.number_of_nodes()} nodes, {G.number_of_edges()} edges",
              fontsize=16, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    
    output_path = OUTPUT_PATH / output_file
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_path}")
    plt.close()

def visualize_circular_layout(G, output_file="graph_circular.png"):
    """Create circular layout visualization"""
    print("\nCreating circular layout visualization...")
    
    plt.figure(figsize=(14, 14))
    
    # Circular layout
    pos = nx.circular_layout(G)
    
    # Calculate node properties
    degrees = dict(G.degree())
    node_sizes = [300 + degrees[node] * 100 for node in G.nodes()]
    
    # Calculate betweenness centrality for coloring
    centrality = nx.betweenness_centrality(G)
    node_colors = [centrality[node] for node in G.nodes()]
    
    # Draw edges with varying transparency based on weight
    for edge in G.edges():
        x = [pos[edge[0]][0], pos[edge[1]][0]]
        y = [pos[edge[0]][1], pos[edge[1]][1]]
        plt.plot(x, y, 'gray', alpha=0.3, linewidth=1.5)
    
    # Draw nodes
    nodes = nx.draw_networkx_nodes(G, pos,
                                   node_color=node_colors,
                                   node_size=node_sizes,
                                   cmap='plasma',
                                   alpha=0.9,
                                   edgecolors='black',
                                   linewidths=2)
    
    # Draw labels
    labels = nx.get_node_attributes(G, 'label')
    if not labels:
        labels = {node: str(node) for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
    
    # Add colorbar
    plt.colorbar(nodes, label='Betweenness Centrality', shrink=0.8)
    
    plt.title(f"Network Graph - Circular Layout\n{G.number_of_nodes()} nodes, {G.number_of_edges()} edges",
              fontsize=16, fontweight='bold', pad=20)
    plt.axis('off')
    plt.axis('equal')
    plt.tight_layout()
    
    output_path = OUTPUT_PATH / output_file
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_path}")
    plt.close()

def visualize_kamada_kawai_layout(G, output_file="graph_kamada_kawai.png"):
    """Create Kamada-Kawai layout visualization"""
    print("\nCreating Kamada-Kawai layout visualization...")
    
    plt.figure(figsize=(14, 14))
    
    try:
        # Kamada-Kawai layout (good for small to medium graphs)
        pos = nx.kamada_kawai_layout(G)
    except:
        print("Kamada-Kawai failed, using spring layout")
        pos = nx.spring_layout(G, seed=42)
    
    # Calculate node properties
    degrees = dict(G.degree())
    node_sizes = [300 + degrees[node] * 100 for node in G.nodes()]
    
    # Calculate clustering coefficient for coloring
    clustering = nx.clustering(G)
    node_colors = [clustering[node] for node in G.nodes()]
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, alpha=0.3, width=2, edge_color='#888888')
    
    # Draw nodes
    nodes = nx.draw_networkx_nodes(G, pos,
                                   node_color=node_colors,
                                   node_size=node_sizes,
                                   cmap='coolwarm',
                                   alpha=0.9,
                                   edgecolors='black',
                                   linewidths=2)
    
    # Draw labels
    labels = nx.get_node_attributes(G, 'label')
    if not labels:
        labels = {node: str(node) for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
    
    # Add colorbar
    plt.colorbar(nodes, label='Clustering Coefficient', shrink=0.8)
    
    plt.title(f"Network Graph - Kamada-Kawai Layout\n{G.number_of_nodes()} nodes, {G.number_of_edges()} edges",
              fontsize=16, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    
    output_path = OUTPUT_PATH / output_file
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_path}")
    plt.close()

def visualize_interactive_network(G, output_file="graph_interactive.html"):
    """Create interactive network visualization with Plotly"""
    print("\nCreating interactive network visualization...")
    
    # Use spring layout for positions
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Create edge trace
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines')
    
    # Create node trace
    node_x = []
    node_y = []
    node_text = []
    node_colors = []
    node_sizes = []
    
    degrees = dict(G.degree())
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        label = G.nodes[node].get('label', str(node))
        degree = degrees[node]
        node_text.append(f"Node: {label}<br>Degree: {degree}")
        node_colors.append(degree)
        node_sizes.append(10 + degree * 3)
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=[G.nodes[node].get('label', str(node)) for node in G.nodes()],
        textposition="top center",
        textfont=dict(size=8),
        hovertext=node_text,
        marker=dict(
            showscale=True,
            colorscale='Viridis',
            size=node_sizes,
            color=node_colors,
            colorbar=dict(
                title="Node<br>Degree",
                xanchor='left'
            ),
            line=dict(width=2, color='white')
        ))
    
    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                       title=dict(
                           text=f'Interactive Network Graph<br>{G.number_of_nodes()} nodes, {G.number_of_edges()} edges',
                           x=0.5,
                           xanchor='center',
                           font=dict(size=20)
                       ),
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=20, l=5, r=5, t=80),
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       width=1200,
                       height=900
                   ))
    
    output_path = OUTPUT_PATH / output_file
    fig.write_html(str(output_path))
    print(f"Saved: {output_path}")

def analyze_graph(G):
    """Perform basic graph analysis"""
    print("\n" + "="*60)
    print("GRAPH ANALYSIS")
    print("="*60)
    
    print(f"Number of nodes: {G.number_of_nodes()}")
    print(f"Number of edges: {G.number_of_edges()}")
    print(f"Average degree: {sum(dict(G.degree()).values()) / G.number_of_nodes():.2f}")
    print(f"Density: {nx.density(G):.4f}")
    print(f"Is connected: {nx.is_connected(G)}")
    
    if nx.is_connected(G):
        print(f"Average shortest path length: {nx.average_shortest_path_length(G):.2f}")
        print(f"Diameter: {nx.diameter(G)}")
    
    print(f"Average clustering coefficient: {nx.average_clustering(G):.4f}")
    
    # Find most central nodes
    degree_centrality = nx.degree_centrality(G)
    top_nodes = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    print("\nTop 5 nodes by degree centrality:")
    for node, centrality in top_nodes:
        label = G.nodes[node].get('label', str(node))
        print(f"  {label}: {centrality:.4f}")

def main():
    """Main execution function"""
    print("="*60)
    print("GRAPH NETWORK VISUALIZATIONS")
    print("="*60)
    
    # Load data - using Ring25.net as example
    G = load_graph_data("Ring25.net")
    
    # Analyze graph
    analyze_graph(G)
    
    # Generate visualizations
    print("\n" + "="*60)
    print("GENERATING VISUALIZATIONS")
    print("="*60)
    
    visualize_spring_layout(G)
    visualize_circular_layout(G)
    visualize_kamada_kawai_layout(G)
    visualize_interactive_network(G)
    
    print("\n" + "="*60)
    print("Graph visualizations completed!")
    print("="*60)

if __name__ == "__main__":
    main()
