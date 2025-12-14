"""
Geospatial Map Visualizations
Creates geospatial visualizations using different layouts
"""

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
from shapely.geometry import Point
import folium
from folium.plugins import HeatMap, MarkerCluster
import numpy as np
from pathlib import Path

# Set up paths
BASE_PATH = Path(__file__).parent.parent
DATA_PATH = BASE_PATH / "datasets" / "map"
OUTPUT_PATH = BASE_PATH / "outputs"
OUTPUT_PATH.mkdir(exist_ok=True)

def load_map_data():
    """Load world cities dataset"""
    print("Loading world cities data...")
    df = pd.read_csv(DATA_PATH / "worldcities.csv")
    
    print(f"Loaded {len(df)} cities")
    print(f"\nDataset columns: {df.columns.tolist()}")
    print(f"\nSample data:\n{df.head()}")
    print(f"\nData info:")
    print(f"  Countries: {df['country'].nunique()}")
    print(f"  Cities with population data: {df['population'].notna().sum()}")
    print(f"  Latitude range: [{df['lat'].min():.2f}, {df['lat'].max():.2f}]")
    print(f"  Longitude range: [{df['lng'].min():.2f}, {df['lng'].max():.2f}]")
    
    return df

def create_geodataframe(df):
    """Convert DataFrame to GeoDataFrame"""
    geometry = [Point(xy) for xy in zip(df['lng'], df['lat'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')
    return gdf

def visualize_static_scatter_map(df, output_file="map_static_scatter.png"):
    """Create static scatter map with matplotlib"""
    print("\nCreating static scatter map...")
    
    # Filter to major cities (population > 1 million)
    df_filtered = df[df['population'] > 1000000].copy()
    df_filtered = df_filtered.dropna(subset=['population'])
    
    fig, ax = plt.subplots(figsize=(20, 12))
    
    # Create a simple world outline using a simple approach
    # Draw background
    ax.set_facecolor('#e6f2ff')
    
    # Create scatter plot
    scatter = ax.scatter(df_filtered['lng'], 
                        df_filtered['lat'],
                        s=df_filtered['population'] / 50000,  # Size by population
                        c=df_filtered['population'],  # Color by population
                        cmap='YlOrRd',
                        alpha=0.6,
                        edgecolors='black',
                        linewidth=0.5)
    
    # Add labels for top 20 cities
    top_cities = df_filtered.nlargest(20, 'population')
    for _, city in top_cities.iterrows():
        ax.annotate(city['city_ascii'],
                   xy=(city['lng'], city['lat']),
                   xytext=(5, 5),
                   textcoords='offset points',
                   fontsize=7,
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                   fontweight='bold')
    
    # Colorbar
    cbar = plt.colorbar(scatter, ax=ax, fraction=0.03, pad=0.04)
    cbar.set_label('Population', rotation=270, labelpad=20, fontsize=12)
    
    ax.set_xlabel('Longitude', fontsize=12, fontweight='bold')
    ax.set_ylabel('Latitude', fontsize=12, fontweight='bold')
    ax.set_title(f'World Cities - Static Scatter Map\n{len(df_filtered)} cities with population > 1M',
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xlim([-180, 180])
    ax.set_ylim([-90, 90])
    ax.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    
    output_path = OUTPUT_PATH / output_file
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_path}")
    plt.close()

def visualize_choropleth_map(df, output_file="map_choropleth.png"):
    """Create density map showing cities by region"""
    print("\nCreating density/hexbin map...")
    
    # Filter valid coordinates
    df_filtered = df.dropna(subset=['lat', 'lng'])
    
    fig, ax = plt.subplots(figsize=(20, 12))
    
    # Create hexbin plot (density map)
    hexbin = ax.hexbin(df_filtered['lng'], 
                       df_filtered['lat'],
                       gridsize=50,
                       cmap='YlOrRd',
                       mincnt=1,
                       alpha=0.8,
                       edgecolors='none')
    
    # Colorbar
    cbar = plt.colorbar(hexbin, ax=ax, fraction=0.03, pad=0.04)
    cbar.set_label('City Density', rotation=270, labelpad=20, fontsize=12)
    
    ax.set_facecolor('#e6f2ff')
    ax.set_xlabel('Longitude', fontsize=12, fontweight='bold')
    ax.set_ylabel('Latitude', fontsize=12, fontweight='bold')
    ax.set_title('World Cities - Density Hexbin Map\nCity Distribution Across the Globe',
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xlim([-180, 180])
    ax.set_ylim([-90, 90])
    ax.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    
    output_path = OUTPUT_PATH / output_file
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_path}")
    plt.close()

def visualize_interactive_plotly_map(df, output_file="map_interactive_plotly.html"):
    """Create interactive map with Plotly"""
    print("\nCreating interactive Plotly map...")
    
    # Filter to cities with population data
    df_filtered = df[df['population'].notna()].copy()
    df_filtered = df_filtered[df_filtered['population'] > 500000]  # > 500k population
    
    # Create figure
    fig = px.scatter_geo(df_filtered,
                        lat='lat',
                        lon='lng',
                        hover_name='city',
                        hover_data={
                            'country': True,
                            'population': ':,',
                            'lat': ':.2f',
                            'lng': ':.2f'
                        },
                        size='population',
                        color='population',
                        color_continuous_scale='Viridis',
                        size_max=30,
                        title=f'World Cities Interactive Map<br>{len(df_filtered)} cities with population > 500K')
    
    fig.update_layout(
        geo=dict(
            showland=True,
            landcolor='rgb(243, 243, 243)',
            coastlinecolor='rgb(204, 204, 204)',
            projection_type='natural earth',
            showlakes=True,
            lakecolor='rgb(230, 245, 255)',
            showcountries=True,
            countrycolor='rgb(204, 204, 204)'
        ),
        title={
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18}
        },
        width=1400,
        height=800,
        margin=dict(l=0, r=0, t=80, b=0)
    )
    
    output_path = OUTPUT_PATH / output_file
    fig.write_html(str(output_path))
    print(f"Saved: {output_path}")

def visualize_folium_heatmap(df, output_file="map_heatmap_folium.html"):
    """Create heatmap with Folium"""
    print("\nCreating Folium heatmap...")
    
    # Filter to cities with population data
    df_filtered = df[df['population'].notna()].copy()
    
    # Create base map
    m = folium.Map(location=[20, 0], zoom_start=2, tiles='OpenStreetMap')
    
    # Prepare data for heatmap (lat, lng, weight)
    heat_data = [[row['lat'], row['lng'], row['population']] 
                 for _, row in df_filtered.iterrows() if row['population'] > 0]
    
    # Add heatmap layer
    HeatMap(heat_data,
            min_opacity=0.3,
            max_opacity=0.8,
            radius=15,
            blur=20,
            gradient={0.4: 'blue', 0.6: 'lime', 0.8: 'yellow', 1.0: 'red'}).add_to(m)
    
    # Add title
    title_html = '''
    <div style="position: fixed; 
                top: 10px; left: 50px; width: 400px; height: 50px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:16px; font-weight: bold; padding: 10px">
        World Cities Population Heatmap
    </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    output_path = OUTPUT_PATH / output_file
    m.save(str(output_path))
    print(f"Saved: {output_path}")

def visualize_folium_cluster_map(df, output_file="map_cluster_folium.html"):
    """Create cluster map with Folium"""
    print("\nCreating Folium cluster map...")
    
    # Filter to major cities
    df_filtered = df[df['population'] > 1000000].copy()
    df_filtered = df_filtered.dropna(subset=['population'])
    
    # Create base map
    m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron')
    
    # Create marker cluster
    marker_cluster = MarkerCluster().add_to(m)
    
    # Add markers
    for _, row in df_filtered.iterrows():
        popup_text = f"""
        <b>{row['city']}</b><br>
        Country: {row['country']}<br>
        Population: {row['population']:,.0f}<br>
        Coordinates: ({row['lat']:.2f}, {row['lng']:.2f})
        """
        
        folium.Marker(
            location=[row['lat'], row['lng']],
            popup=folium.Popup(popup_text, max_width=250),
            tooltip=row['city'],
            icon=folium.Icon(color='red' if row['capital'] == 'primary' else 'blue',
                           icon='info-sign')
        ).add_to(marker_cluster)
    
    # Add title
    title_html = '''
    <div style="position: fixed; 
                top: 10px; left: 50px; width: 450px; height: 50px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:16px; font-weight: bold; padding: 10px">
        World Cities Cluster Map (Population > 1M)
    </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    output_path = OUTPUT_PATH / output_file
    m.save(str(output_path))
    print(f"Saved: {output_path}")

def analyze_spatial_data(df):
    """Perform basic spatial analysis"""
    print("\n" + "="*60)
    print("SPATIAL DATA ANALYSIS")
    print("="*60)
    
    print(f"Total cities: {len(df)}")
    print(f"Countries represented: {df['country'].nunique()}")
    print(f"\nTop 10 countries by city count:")
    print(df['country'].value_counts().head(10))
    
    print(f"\n Cities with population data: {df['population'].notna().sum()}")
    if df['population'].notna().sum() > 0:
        print(f"Average city population: {df['population'].mean():,.0f}")
        print(f"Largest city: {df.loc[df['population'].idxmax(), 'city']} "
              f"({df['population'].max():,.0f})")
    
    print(f"\nCapital cities: {(df['capital'] == 'primary').sum()}")
    
    # Hemisphere distribution
    north = (df['lat'] > 0).sum()
    south = (df['lat'] <= 0).sum()
    east = (df['lng'] > 0).sum()
    west = (df['lng'] <= 0).sum()
    
    print(f"\nHemisphere distribution:")
    print(f"  Northern: {north} ({north/len(df)*100:.1f}%)")
    print(f"  Southern: {south} ({south/len(df)*100:.1f}%)")
    print(f"  Eastern: {east} ({east/len(df)*100:.1f}%)")
    print(f"  Western: {west} ({west/len(df)*100:.1f}%)")

def main():
    """Main execution function"""
    print("="*60)
    print("GEOSPATIAL MAP VISUALIZATIONS")
    print("="*60)
    
    # Load data
    df = load_map_data()
    
    # Analyze spatial data
    analyze_spatial_data(df)
    
    # Generate visualizations
    print("\n" + "="*60)
    print("GENERATING VISUALIZATIONS")
    print("="*60)
    
    visualize_static_scatter_map(df)
    visualize_choropleth_map(df)
    visualize_interactive_plotly_map(df)
    visualize_folium_heatmap(df)
    visualize_folium_cluster_map(df)
    
    print("\n" + "="*60)
    print("Map visualizations completed!")
    print("="*60)

if __name__ == "__main__":
    main()
