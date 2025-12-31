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
        """Initialize empty graph"""
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
    
    def add_transaction(self, items):
        """
        Add a transaction (dynamic update)
        
        Args:
            items: List of items (one basket)
        """
        # Deduplicate items in basket
        unique_items = list(set(items))
        
        # Update item set
        self.items.update(unique_items)
        
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
