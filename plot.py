import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

def load_csv(filepath):
    """Load CSV file and return dataframe"""
    try:
        df = pd.read_csv(filepath)
        print(f"✓ Loaded {filepath}")
        print(f"  Columns: {list(df.columns)}")
        print(f"  Rows: {len(df)}")
        return df
    except FileNotFoundError:
        print(f"✗ Error: File '{filepath}' not found")
        return None
    except Exception as e:
        print(f"✗ Error loading CSV: {e}")
        return None

def plot_graph(df, x_col=None, y_col=None, plot_type='line', title=None, xlabel=None, ylabel=None, output=None):
    """
    Create and display/save a plot
    
    Parameters:
    - df: pandas DataFrame
    - x_col: Column name for X axis (default: first column)
    - y_col: Column name for Y axis (default: second column)
    - plot_type: Type of plot ('line', 'scatter', 'bar', 'hist', 'box')
    - title: Plot title
    - xlabel: X axis label
    - ylabel: Y axis label
    - output: Path to save the plot (e.g., 'graph.png')
    """
    
    if df is None or df.empty:
        print("✗ No data to plot")
        return
    
    # Auto-select columns if not specified
    if x_col is None:
        x_col = df.columns[0]
    if y_col is None:
        y_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
    
    # Check if columns exist
    if x_col not in df.columns or y_col not in df.columns:
        print(f"✗ Column not found. Available: {list(df.columns)}")
        return
    
    # Create figure and plot
    plt.figure(figsize=(10, 6))
    
    try:
        if plot_type == 'line':
            plt.plot(df[x_col], df[y_col], marker='o', linestyle='-', linewidth=2)
        elif plot_type == 'scatter':
            plt.scatter(df[x_col], df[y_col], alpha=0.6, s=100)
        elif plot_type == 'bar':
            plt.bar(df[x_col], df[y_col], alpha=0.7)
        elif plot_type == 'hist':
            plt.hist(df[y_col], bins=20, alpha=0.7, edgecolor='black')
        elif plot_type == 'box':
            plt.boxplot(df[y_col])
        else:
            print(f"✗ Unknown plot type: {plot_type}")
            return
        
        # Add labels and title
        plt.xlabel(xlabel or x_col, fontsize=12)
        plt.ylabel(ylabel or y_col, fontsize=12)
        plt.title(title or f"{y_col} vs {x_col}", fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Save or show
        if output:
            plt.savefig(output, dpi=300, bbox_inches='tight')
            print(f"✓ Plot saved to '{output}'")
        else:
            plt.show()
            
    except Exception as e:
        print(f"✗ Error creating plot: {e}")
    finally:
        plt.close()

def main():
    parser = argparse.ArgumentParser(description='Quick CSV to Graph Plotter')
    parser.add_argument('--csv', required=True, help='Path to CSV file')
    parser.add_argument('--x', help='Column name for X axis')
    parser.add_argument('--y', help='Column name for Y axis')
    parser.add_argument('--type', default='line', choices=['line', 'scatter', 'bar', 'hist', 'box'],
                       help='Type of plot (default: line)')
    parser.add_argument('--title', help='Plot title')
    parser.add_argument('--xlabel', help='X axis label')
    parser.add_argument('--ylabel', help='Y axis label')
    parser.add_argument('--output', help='Output file path (e.g., graph.png)')
    
    args = parser.parse_args()
    
    # Load data
    df = load_csv(args.csv)
    
    # Create plot
    if df is not None:
        plot_graph(
            df,
            x_col=args.x,
            y_col=args.y,
            plot_type=args.type,
            title=args.title,
            xlabel=args.xlabel,
            ylabel=args.ylabel,
            output=args.output
        )

if __name__ == '__main__':
    main()
