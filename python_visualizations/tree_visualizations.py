"""
Tree of Life Visualizations
Creates hierarchical visualizations using different layouts
"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from pathlib import Path

# Set up paths
BASE_PATH = Path(__file__).parent.parent
DATA_PATH = BASE_PATH / "datasets" / "tree"
OUTPUT_PATH = BASE_PATH / "outputs"
OUTPUT_PATH.mkdir(exist_ok=True)

def load_tree_data():
    """Load tree of life dataset"""
    print("Loading tree of life data...")
    nodes_df = pd.read_csv(DATA_PATH / "treeoflife_nodes.csv")
    links_df = pd.read_csv(DATA_PATH / "treeoflife_links.csv")
    
    print(f"Loaded {len(nodes_df)} nodes and {len(links_df)} edges")
    print(f"\nSample nodes:\n{nodes_df.head()}")
    print(f"\nSample links:\n{links_df.head()}")
    
    return nodes_df, links_df

def create_networkx_graph(nodes_df, links_df):
    """Create NetworkX directed graph from the data"""
    G = nx.DiGraph()
    
    # Add nodes with attributes
    for _, row in nodes_df.iterrows():
        G.add_node(row['node_id'], 
                   name=row['node_name'],
                   leaf=row['leaf_node'],
                   extinct=row['extinct'])
    
    # Add edges
    for _, row in links_df.iterrows():
        G.add_edge(row['source_node_id'], row['target_node_id'])
    
    return G

def get_subtree(G, root_node, max_depth=3):
    """Extract a subtree starting from root_node up to max_depth"""
    nodes_at_depth = {root_node}
    subtree_nodes = {root_node}
    
    for depth in range(max_depth):
        next_level = set()
        for node in nodes_at_depth:
            successors = set(G.successors(node))
            next_level.update(successors)
        subtree_nodes.update(next_level)
        nodes_at_depth = next_level
        if not next_level:
            break
    
    return G.subgraph(subtree_nodes).copy()

def visualize_radial_tree(G, nodes_df, output_file="tree_radial.png"):
    """Create a radial (circular) tree layout visualization"""
    print("\nCreating radial tree visualization...")
    
    # Get a manageable subtree (from root, depth 3)
    subtree = get_subtree(G, 1, max_depth=3)
    
    # Use hierarchical layout
    pos = nx.spring_layout(subtree, k=2, iterations=50, seed=42)
    
    # Create figure
    plt.figure(figsize=(16, 16))
    
    # Draw nodes
    node_colors = []
    for node in subtree.nodes():
        if subtree.nodes[node].get('extinct', 0) == 1:
            node_colors.append('#ff6b6b')  # Red for extinct
        elif subtree.nodes[node].get('leaf', 0) == 1:
            node_colors.append('#51cf66')  # Green for leaf nodes
        else:
            node_colors.append('#4dabf7')  # Blue for internal nodes
    
    # Draw edges
    nx.draw_networkx_edges(subtree, pos, alpha=0.3, 
                           arrows=True, arrowsize=10,
                           edge_color='gray', width=1.5)
    
    # Draw nodes
    nx.draw_networkx_nodes(subtree, pos, 
                          node_color=node_colors,
                          node_size=500, alpha=0.9,
                          edgecolors='black', linewidths=1)
    
    # Draw labels for important nodes
    labels = {}
    for node in subtree.nodes():
        if subtree.in_degree(node) == 0 or subtree.out_degree(node) > 5:
            labels[node] = subtree.nodes[node].get('name', str(node))[:20]
    
    nx.draw_networkx_labels(subtree, pos, labels, font_size=8, font_weight='bold')
    
    plt.title("Tree of Life - Radial Layout\n(Subset: Root to Depth 3)", 
              fontsize=18, fontweight='bold', pad=20)
    
    # Add legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#4dabf7', 
                   markersize=10, label='Internal Node'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#51cf66', 
                   markersize=10, label='Leaf Node'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#ff6b6b', 
                   markersize=10, label='Extinct')
    ]
    plt.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    plt.axis('off')
    plt.tight_layout()
    
    output_path = OUTPUT_PATH / output_file
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_path}")
    plt.close()

def visualize_hierarchical_tree(G, nodes_df, output_file="tree_hierarchical.png"):
    """Create a hierarchical (top-down) tree layout visualization"""
    print("\nCreating hierarchical tree visualization...")
    
    # Get a manageable subtree
    subtree = get_subtree(G, 1, max_depth=4)
    
    # Use hierarchical positions
    def hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
        """Create hierarchical layout positions"""
        pos = {root: (xcenter, vert_loc)}
        neighbors = list(G.successors(root))
        if len(neighbors) != 0:
            dx = width / len(neighbors)
            nextx = xcenter - width/2 - dx/2
            for neighbor in neighbors:
                nextx += dx
                pos.update(hierarchy_pos(G, neighbor, 
                                        width=dx, vert_gap=vert_gap,
                                        vert_loc=vert_loc-vert_gap, 
                                        xcenter=nextx))
        return pos
    
    try:
        pos = hierarchy_pos(subtree, 1)
    except:
        pos = nx.spring_layout(subtree, seed=42)
    
    # Create figure
    plt.figure(figsize=(20, 12))
    
    # Determine node colors
    node_colors = []
    node_sizes = []
    for node in subtree.nodes():
        out_degree = subtree.out_degree(node)
        
        if subtree.nodes[node].get('extinct', 0) == 1:
            node_colors.append('#ff6b6b')
        elif subtree.nodes[node].get('leaf', 0) == 1:
            node_colors.append('#51cf66')
        else:
            node_colors.append('#4dabf7')
        
        # Size based on number of children
        node_sizes.append(300 + out_degree * 50)
    
    # Draw edges
    nx.draw_networkx_edges(subtree, pos, alpha=0.3,
                           arrows=True, arrowsize=15,
                           edge_color='gray', width=2)
    
    # Draw nodes
    nx.draw_networkx_nodes(subtree, pos,
                          node_color=node_colors,
                          node_size=node_sizes,
                          alpha=0.9,
                          edgecolors='black',
                          linewidths=1.5)
    
    # Draw labels for key nodes
    labels = {}
    for node in subtree.nodes():
        if subtree.in_degree(node) == 0 or subtree.out_degree(node) >= 3:
            name = subtree.nodes[node].get('name', str(node))
            labels[node] = name[:25]
    
    nx.draw_networkx_labels(subtree, pos, labels, font_size=7, font_weight='bold')
    
    plt.title("Tree of Life - Hierarchical Layout\n(Top-Down View, Depth 4)", 
              fontsize=18, fontweight='bold', pad=20)
    
    # Legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#4dabf7',
                   markersize=12, label='Internal Node'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#51cf66',
                   markersize=12, label='Leaf Node'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#ff6b6b',
                   markersize=12, label='Extinct')
    ]
    plt.legend(handles=legend_elements, loc='upper right', fontsize=11)
    
    plt.axis('off')
    plt.tight_layout()
    
    output_path = OUTPUT_PATH / output_file
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_path}")
    plt.close()

def visualize_sunburst_interactive(G, nodes_df, output_file="tree_sunburst.html"):
    """Create an interactive sunburst diagram"""
    print("\nCreating interactive sunburst visualization...")
    
    # Get a manageable subtree
    subtree = get_subtree(G, 1, max_depth=5)
    
    # Build hierarchical data for sunburst
    ids = []
    labels = []
    parents = []
    values = []
    colors = []
    
    for node in subtree.nodes():
        node_name = subtree.nodes[node].get('name', str(node))
        ids.append(str(node))
        labels.append(node_name[:30])
        
        # Find parent
        predecessors = list(subtree.predecessors(node))
        if predecessors:
            parents.append(str(predecessors[0]))
        else:
            parents.append("")
        
        # Value based on number of descendants
        descendants = len(list(nx.descendants(subtree, node)))
        values.append(descendants + 1)
        
        # Color based on node type
        if subtree.nodes[node].get('extinct', 0) == 1:
            colors.append('#ff6b6b')
        elif subtree.nodes[node].get('leaf', 0) == 1:
            colors.append('#51cf66')
        else:
            colors.append('#4dabf7')
    
    fig = go.Figure(go.Sunburst(
        ids=ids,
        labels=labels,
        parents=parents,
        values=values,
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        branchvalues="total",
        hovertemplate='<b>%{label}</b><br>Descendants: %{value}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': "Tree of Life - Interactive Sunburst Diagram",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Arial Black'}
        },
        width=1000,
        height=1000,
        margin=dict(t=100, l=0, r=0, b=0)
    )
    
    output_path = OUTPUT_PATH / output_file
    fig.write_html(str(output_path))
    print(f"Saved: {output_path}")

def main():
    """Main execution function"""
    print("="*60)
    print("TREE OF LIFE VISUALIZATIONS")
    print("="*60)
    
    # Load data
    nodes_df, links_df = load_tree_data()
    
    # Create graph
    G = create_networkx_graph(nodes_df, links_df)
    print(f"\nGraph created: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    
    # Generate visualizations
    visualize_radial_tree(G, nodes_df)
    visualize_hierarchical_tree(G, nodes_df)
    visualize_sunburst_interactive(G, nodes_df)
    
    print("\n" + "="*60)
    print("Tree visualizations completed!")
    print("="*60)

if __name__ == "__main__":
    main()
