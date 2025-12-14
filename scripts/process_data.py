import pandas as pd
import networkx as nx
import json
import os
from pathlib import Path
import re

# Paths
BASE_DIR = Path(__file__).parent.parent
DATASETS_DIR = BASE_DIR / "datasets"
OUTPUT_DIR = BASE_DIR / "dashboard" / "public" / "data"

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def process_tree_data():
    print("Processing Tree Data...")
    nodes_path = DATASETS_DIR / "tree" / "treeoflife_nodes.csv"
    links_path = DATASETS_DIR / "tree" / "treeoflife_links.csv"
    
    nodes_df = pd.read_csv(nodes_path)
    links_df = pd.read_csv(links_path)
    
    # Build a dictionary of nodes for quick lookup
    nodes_dict = {}
    for _, row in nodes_df.iterrows():
        nodes_dict[row['node_id']] = {
            "name": row['node_name'],
            "attributes": {
                "leaf": bool(row['leaf_node']),
                "extinct": bool(row['extinct']),
                "confidence": row.get('confidence', None)
            },
            "children": []
        }
    
    # Build hierarchy
    # We need to find the root. Assuming node_id 1 is root or we can infer from links.
    # links have source and target.
    
    # Create an adjacency list basically
    # But for a specific hierarchical structure (like D3 hierarchy), it's often better to have a recursive structure
    
    # Let's verify if it's a single root tree.
    # Root has no incoming edges.
    all_targets = set(links_df['target_node_id'])
    all_nodes = set(nodes_df['node_id'])
    potential_roots = all_nodes - all_targets
    
    print(f"Found {len(potential_roots)} potential roots.")
    
    # For simplicity, we'll build the tree starting from these roots.
    # If multiple roots, we can create a dummy super-root or just take the first one (often 'Life')
    
    # Helper to build recursive tree
    def build_subtree(node_id, current_depth=0, max_depth=3):
        node = nodes_dict.get(node_id)
        if not node:
            return None
        
        # Stop at max_depth
        if current_depth >= max_depth:
             return {
                "name": node['name'],
                **node['attributes'],
                "value": 1
            }

        # specific to this dataset: find children
        children_ids = links_df[links_df['source_node_id'] == node_id]['target_node_id'].tolist()
        
        children = []
        for child_id in children_ids:
            child_node = build_subtree(child_id, current_depth + 1, max_depth)
            if child_node:
                children.append(child_node)
        
        result = {
            "name": node['name'],
            **node['attributes'],
        }
        
        if children:
            result["children"] = children
        else:
            result["value"] = 1 
            
        return result

    # Assuming node 1 is the main root based on previous analysis (Life on Earth)
    # If uncertain, we can use the potential_roots
    root_id = 1
    if root_id not in nodes_dict:
        if len(potential_roots) > 0:
            root_id = list(potential_roots)[0]
    
    # Reduced depth for performance (was full tree ~36k nodes)
    print("Building subtree with max_depth=3...")
    tree_data = build_subtree(root_id, max_depth=3)
    
    with open(OUTPUT_DIR / "tree.json", "w") as f:
        json.dump(tree_data, f)
    print("Tree data saved to tree.json")

def parse_pajek_net_file(filepath):
    """Simple parser for Pajek .net files (reused logic)"""
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
            parts = line.split()
            if len(parts) >= 2:
                node_id = int(parts[0])
                label_match = re.search(r'"([^"]*)"', line)
                label = label_match.group(1) if label_match else parts[1]
                G.add_node(node_id, label=label, id=node_id)
        
        elif mode == 'edges' and line:
            parts = line.split()
            if len(parts) >= 2:
                source = int(parts[0])
                target = int(parts[1])
                weight = float(parts[2]) if len(parts) > 2 else 1.0
                G.add_edge(source, target, weight=weight)
    return G

def process_graph_data():
    print("Processing Graph Data...")
    net_path = DATASETS_DIR / "graph" / "Ring25.net"
    
    G = parse_pajek_net_file(net_path)
    
    # Calculate layout positions (Spring) - pre-calculating can save frontend effort, 
    # but react-force-graph usually handles it. 
    # However, let's just export nodes and links with attributes.
    
    # Add some centrality metrics
    degree = dict(G.degree())
    try:
        betweenness = nx.betweenness_centrality(G)
    except:
        betweenness = {}
    
    nodes = []
    for node_id, data in G.nodes(data=True):
        nodes.append({
            "id": node_id,
            "label": data.get('label', str(node_id)),
            "val": degree.get(node_id, 1), # for node size
            "group": int(degree.get(node_id, 1)), # for color grouping
            "centrality": betweenness.get(node_id, 0)
        })
        
    links = []
    for u, v, data in G.edges(data=True):
        links.append({
            "source": u,
            "target": v,
            "value": data.get('weight', 1)
        })
        
    graph_data = {
        "nodes": nodes,
        "links": links
    }
    
    with open(OUTPUT_DIR / "network.json", "w") as f:
        json.dump(graph_data, f)
    print("Graph data saved to network.json")

def process_map_data():
    print("Processing Map Data...")
    csv_path = DATASETS_DIR / "map" / "worldcities.csv"
    df = pd.read_csv(csv_path)
    
    # Filter for major cities to keep file size manageable for frontend
    # INCREASED THRESHOLD: Population > 1,000,000 or capitals (was 100k)
    major_cities = df[
        (df['population'] > 1000000) | 
        (df['capital'] == 'primary')
    ].copy()
    
    # Handle NaN population
    major_cities['population'] = major_cities['population'].fillna(0)
    
    print(f"Filtered map cities from {len(df)} to {len(major_cities)}")
    
    features = []
    for _, row in major_cities.iterrows():
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row['lng'], row['lat']]
            },
            "properties": {
                "city": row['city'],
                "country": row['country'],
                "population": row['population'],
                "capital": row['capital'] if pd.notna(row['capital']) else None,
                "iso2": row['iso2'] if pd.notna(row['iso2']) else None,
                "iso3": row['iso3'] if pd.notna(row['iso3']) else None
            }
        }
        features.append(feature)
        
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    with open(OUTPUT_DIR / "cities.json", "w") as f: # standard json extension often easier
        json.dump(geojson, f)
    print("Map data saved to cities.json")

def main():
    try:
        process_tree_data()
    except Exception as e:
        print(f"Error processing tree: {e}")
        
    try:
        process_graph_data()
    except Exception as e:
        print(f"Error processing graph: {e}")
        
    try:
        process_map_data()
    except Exception as e:
        print(f"Error processing map: {e}")

if __name__ == "__main__":
    main()
