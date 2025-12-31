"""
Abstract base class for graph data structures.

Defines the interface contract that all graph implementations must follow,
enabling dependency inversion and open/closed principles.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Tuple


class Graph(ABC):
    """
    Abstract base class for graph data structures.
    
    This interface enables polymorphism - any concrete implementation
    (adjacency list, adjacency matrix, edge list) can be used interchangeably
    in the RecommendationEngine without code changes.
    
    Design Principle: Dependency Inversion Principle (DIP)
    - High-level modules (RecommendationEngine) depend on this abstraction
    - Low-level modules (GraphAdjacencyList) implement this abstraction
    """
    
    @abstractmethod
    def build_from_csv(self, csv_path: str) -> None:
        """
        Build graph from CSV dataset.
        
        Args:
            csv_path: Path to CSV file
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
        """
        pass
    
    @abstractmethod
    def add_transaction(self, items: List[str]) -> None:
        """
        Add a transaction to the graph (dynamic update).
        
        Args:
            items: List of items in the transaction basket
        """
        pass
    
    @abstractmethod
    def get_neighbors(self, item: str) -> Dict[str, int]:
        """
        Get all neighbors of an item with co-occurrence counts.
        
        Args:
            item: Item name
            
        Returns:
            Dictionary mapping neighbor items to co-occurrence counts
            Returns empty dict if item doesn't exist (graceful degradation)
        """
        pass
    
    @abstractmethod
    def get_top_neighbors(self, item: str, top_k: int = 5) -> List[Tuple[str, int]]:
        """
        Get top-K neighbors of an item sorted by co-occurrence frequency.
        
        Args:
            item: Item name
            top_k: Number of neighbors to return
            
        Returns:
            List of (item_name, count) tuples sorted by count descending,
            then by name ascending for stability
        """
        pass
    
    @abstractmethod
    def get_edge_weight(self, item1: str, item2: str) -> int:
        """
        Get co-occurrence count between two items.
        
        Args:
            item1, item2: Item names
            
        Returns:
            Co-occurrence count, 0 if edge doesn't exist
        """
        pass
    
    @abstractmethod
    def has_item(self, item: str) -> bool:
        """
        Check if item exists in graph.
        
        Args:
            item: Item name
            
        Returns:
            True if item exists, False otherwise
        """
        pass
    
    @abstractmethod
    def get_all_items(self) -> List[str]:
        """
        Get all items in the graph.
        
        Returns:
            List of all item names
        """
        pass
    
    @property
    @abstractmethod
    def num_edges(self) -> int:
        """
        Get total number of edges in the graph.
        
        Returns:
            Number of edges (co-occurrence pairs)
        """
        pass
