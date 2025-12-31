"""
Recommendation Engine (Business Logic Layer)

Encapsulates recommendation system business logic, calls Graph layer to implement features

Design Pattern: Dependency Injection - depends on Graph abstraction, not concrete implementation
"""

from typing import Optional
from task2.src.graph_interface import Graph
from task2.src.graph_adjacency_list import GraphAdjacencyList


class RecommendationEngine:
    """
    Recommendation Engine with dependency injection.
    
    Design Principles:
    - Dependency Inversion: Depends on Graph interface, not concrete class
    - Open/Closed: Can accept any Graph implementation without modification
    """
    
    def __init__(self, graph: Optional[Graph] = None):
        """
        Initialize recommendation engine with dependency injection.
        
        Args:
            graph: Graph implementation (defaults to GraphAdjacencyList if not provided)
                   Accepts any class implementing Graph interface (DIP principle)
        """
        self.graph = graph if graph is not None else GraphAdjacencyList()
    
    def load_data(self, csv_path):
        """
        Load data
        
        Args:
            csv_path: Path to CSV file
        """
        self.graph.build_from_csv(csv_path)
    
    def recommend_for_item(self, item, top_k=5):
        """
        Requirement 1: Single item recommendation
        "What else do customers who bought bread buy?"
        
        Args:
            item: Item name
            top_k: Number to return
            
        Returns:
            list[tuple]: [(recommended_item, co-purchase_count), ...]
        """
        return self.graph.get_top_neighbors(item, top_k)
    
    def get_most_frequent_pairs(self, top_k=10):
        """
        Requirement 2: Most frequent co-purchase pairs
        "Which product combinations are most frequently bought together?"
        
        Args:
            top_k: Number to return
            
        Returns:
            list[tuple]: [((item1, item2), count), ...]
        """
        # Collect all edges
        pairs = []
        seen = set()
        
        for item1 in self.graph.get_all_items():
            neighbors = self.graph.get_neighbors(item1)
            for item2, count in neighbors.items():
                # Avoid duplicates: (A,B) and (B,A) are same
                pair_key = tuple(sorted([item1, item2]))
                if pair_key not in seen:
                    seen.add(pair_key)
                    pairs.append((pair_key, count))
        
        # Sort by count descending, then by pair for stability
        sorted_pairs = sorted(pairs, key=lambda x: (-x[1], x[0]))
        return sorted_pairs[:top_k]
    
    def check_co_purchase(self, item1, item2, threshold=50):
        """
        Requirement 3: Co-purchase check
        "Are two items frequently bought together?"
        
        Args:
            item1, item2: Item names
            threshold: Judgment threshold (co-purchase count)
            
        Returns:
            bool: True if frequently co-purchased
        """
        count = self.graph.get_edge_weight(item1, item2)
        return count >= threshold
    
    def recommend_for_basket(self, basket, top_k=5):
        """
        Extended feature: Basket recommendation
        "Recommend items based on current basket"
        
        Args:
            basket: List of selected items
            top_k: Number to return
            
        Returns:
            list[tuple]: [(recommended_item, aggregated_score), ...]
        """
        if not basket:
            return []
        
        # Aggregate scores from all basket items
        from collections import defaultdict
        scores = defaultdict(int)
        
        for item in basket:
            neighbors = self.graph.get_neighbors(item)
            for neighbor, count in neighbors.items():
                if neighbor not in basket:  # Exclude items already in basket
                    scores[neighbor] += count
        
        # Sort by score descending, then by name for stability
        sorted_items = sorted(scores.items(), key=lambda x: (-x[1], x[0]))
        return sorted_items[:top_k]
    
    def update_with_transaction(self, items):
        """
        Extended feature: Dynamic update
        "Update recommendation system in real-time"
        
        Args:
            items: List of items in new transaction
        """
        self.graph.add_transaction(items)
    
    def get_pair_count(self, item1, item2):
        """
        Get co-occurrence count between two items (for testing)
        
        Args:
            item1, item2: Item names
            
        Returns:
            int: Co-occurrence count
        """
        return self.graph.get_edge_weight(item1, item2)
