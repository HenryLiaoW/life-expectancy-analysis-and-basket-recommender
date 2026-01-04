"""
Graph Adjacency List Implementation (Data Structure Layer)

Stores item co-occurrence relationships using dict[str, dict[str, int]]

Design Pattern: Implements Graph interface for dependency inversion
"""

from pathlib import Path
import csv
from collections import defaultdict
from task2.src.graph_interface import Graph


class GraphAdjacencyList(Graph):
    """
    Adjacency list graph data structure implementation.
    
    Implements Graph interface to support polymorphism and SOLID principles.
    """
    
    def __init__(self):
        """Initialize empty graph(allocate spaces for nodes[O(V)] and edges[O(E)])"""
        self.graph = defaultdict(lambda: defaultdict(int))
        self.items = set()
        self._num_edges = 0
    
    @property
    def num_edges(self) -> int:
        """Get total number of edges (implements Graph interface)"""
        return self._num_edges
    
    def build_from_csv(self, csv_path):
        """
        Build graph from CSV file
        
        Args:
            csv_path: Path to CSV file
        """
        csv_file = Path(csv_path)
        if not csv_file.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        # Group items by basket (member, date)
        baskets = defaultdict(list)
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                member = row['Member_number']
                date = row['Date']
                item = row['itemDescription']
                basket_key = (member, date)
                baskets[basket_key].append(item)
        
        # Build graph from baskets
        for basket_items in baskets.values():
            self.add_transaction(basket_items)
    
    def add_transaction(self, items): # the place which stores the edges
        """
        Add a transaction (dynamic update)
        
        Args:
            items: List of items (one basket)
        """
        # Deduplicate items in basket
        unique_items = list(set(items))
        
        # Update item set
        self.items.update(unique_items) # add new items to the set!!!
        
        # Create edges for all pairs
        for i in range(len(unique_items)):
            for j in range(i + 1, len(unique_items)):
                item1, item2 = unique_items[i], unique_items[j]
                # Check if edge is new
                if self.graph[item1][item2] == 0:
                    self._num_edges += 1
                # Symmetric update for undirected graph
                self.graph[item1][item2] += 1
                self.graph[item2][item1] += 1
    
    def get_neighbors(self, item):
        """
        Get all neighbors of an item
        
        Args:
            item: Item name
            
        Returns:
            dict[str, int]: {neighbor_item: co-occurrence_count}
        """
        if item not in self.graph:
            return {}
        return dict(self.graph[item])
    
    def get_top_neighbors(self, item, top_k=5):
        """
        Get top-K neighbors of an item
        
        Args:
            item: Item name
            top_k: Number to return
            
        Returns:
            list[tuple]: [(item, count), ...], sorted by count descending
        """
        neighbors = self.get_neighbors(item)
        if not neighbors:
            return []
        
        # Sort by count descending, then by name for stability
        sorted_neighbors = sorted(neighbors.items(), key=lambda x: (-x[1], x[0]))
        return sorted_neighbors[:top_k]
    
    def get_edge_weight(self, item1, item2):
        """
        Get co-occurrence count between two items
        
        Args:
            item1, item2: Item names
            
        Returns:
            int: Co-occurrence count, 0 if not exists
        """
        return self.graph.get(item1, {}).get(item2, 0)
    
    def has_item(self, item):
        """
        Check if item exists
        
        Args:
            item: Item name
            
        Returns:
            bool: True if exists
        """
        return item in self.items
    
    def get_all_items(self):
        """
        Get all items
        
        Returns:
            list[str]: List of item names
        """
        return list(self.items)
    
    def visualize_subgraph(self, center_item, max_neighbors=10):
        """
        Generate ASCII visualization of item's neighborhood
        
        Args:
            center_item: Central item to visualize
            max_neighbors: Max neighbors to show
            
        Returns:
            str: ASCII visualization or error message
        """
        if not self.has_item(center_item):
            return f"Item '{center_item}' not found"
        
        neighbors = self.get_top_neighbors(center_item, max_neighbors)
        if not neighbors:
            return f"No neighbors found for '{center_item}'"
        
        total_neighbors = len(self.get_neighbors(center_item))
        
        lines = []
        
        # Add notice if actual neighbors less than requested
        if total_neighbors < max_neighbors:
            lines.append(f"\n✓ Found only {total_neighbors} neighbors for '{center_item}'\n")
        
        lines.append(f"{'='*70}")
        lines.append(f"SUBGRAPH VISUALIZATION: {center_item}")
        lines.append(f"{'='*70}")
        lines.append(f"Center Node: [{center_item}]")
        lines.append(f"Total Neighbors: {total_neighbors}")
        lines.append(f"Showing Top {len(neighbors)} Neighbors")
        lines.append(f"{'-'*70}\n")
        
        for i, (neighbor, weight) in enumerate(neighbors, 1):
            bar_length = min(50, int(weight / 5))
            bar = '█' * bar_length
            lines.append(f"{i:2d}. [{neighbor}]")
            lines.append(f"    Edge weight: {weight} {bar}")
            lines.append("")
        
        lines.append(f"{'='*70}\n")
        return '\n'.join(lines)
    
    def export_to_dot(self, output_path, max_edges=100):
        """
        Export graph to DOT format for Graphviz visualization
        
        Args:
            output_path: Path to save .dot file
            max_edges: Limit edges for readability (0 for all)
            
        Returns:
            str: Success message or error
        """
        try:
            # Get top edges by weight for visualization
            all_edges = []
            seen = set()
            
            for item1 in self.graph:
                for item2, weight in self.graph[item1].items():
                    edge = tuple(sorted([item1, item2]))
                    if edge not in seen:
                        seen.add(edge)
                        all_edges.append((edge[0], edge[1], weight))
            
            # Sort by weight and limit
            all_edges.sort(key=lambda x: -x[2])
            if max_edges > 0:
                all_edges = all_edges[:max_edges]
            
            # Generate DOT format
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("graph SupermarketGraph {\n")
                f.write("  graph [rankdir=LR, overlap=false];\n")
                f.write("  node [shape=box, style=filled, fillcolor=lightblue];\n")
                f.write("  edge [color=gray];\n\n")
                
                # Write edges
                for item1, item2, weight in all_edges:
                    # Escape quotes and special chars
                    item1_clean = item1.replace('"', '\\"')
                    item2_clean = item2.replace('"', '\\"')
                    f.write(f'  "{item1_clean}" -- "{item2_clean}" [label="{weight}", penwidth={min(weight/20, 5)}];\n')
                
                f.write("}\n")
            
            return f"✓ Exported {len(all_edges)} edges to {output_path}"
        except Exception as e:
            return f"✗ Export failed: {str(e)}"
