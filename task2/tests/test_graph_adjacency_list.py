"""
Tests for GraphAdjacencyList (Data Structure Layer)

TDD Red Phase: Testing Graph basic functionality and add_transaction method
"""

import pytest
from pathlib import Path
from task2.src.graph_adjacency_list import GraphAdjacencyList


class TestGraphConstruction:
    """Test graph construction"""
    
    def test_build_from_csv_file_not_found(self):
        """Test handling of non-existent CSV file"""
        graph = GraphAdjacencyList()
        
        with pytest.raises(FileNotFoundError):
            graph.build_from_csv('nonexistent.csv')
    
    def test_build_from_csv_creates_graph(self):
        """Test building graph from CSV"""
        graph = GraphAdjacencyList()
        csv_path = Path(__file__).parent.parent / "data" / "Supermarket_dataset_PAI.csv"
        
        graph.build_from_csv(str(csv_path))
        
        # Verify graph is not empty
        assert len(graph.get_all_items()) > 0
        assert graph.num_edges > 0
    
    def test_graph_has_expected_items(self):
        """Test graph contains known items"""
        graph = GraphAdjacencyList()
        csv_path = Path(__file__).parent.parent / "data" / "Supermarket_dataset_PAI.csv"
        graph.build_from_csv(str(csv_path))
        
        # Verify common items exist
        assert graph.has_item('whole milk')
        assert graph.has_item('other vegetables')


class TestGraphQueries:
    """Test graph query operations"""
    
    @pytest.fixture
    def graph(self):
        """Create and load graph"""
        g = GraphAdjacencyList()
        csv_path = Path(__file__).parent.parent / "data" / "Supermarket_dataset_PAI.csv"
        g.build_from_csv(str(csv_path))
        return g
    
    def test_get_neighbors_returns_dict(self, graph):
        """Test get_neighbors returns dictionary"""
        neighbors = graph.get_neighbors('whole milk')
        
        assert isinstance(neighbors, dict)
        assert len(neighbors) > 0
    
    def test_get_top_neighbors_returns_sorted_list(self, graph):
        """Test Top-K neighbors sorted by frequency"""
        top5 = graph.get_top_neighbors('whole milk', 5)
        
        assert len(top5) == 5
        # Verify descending order
        for i in range(len(top5) - 1):
            assert top5[i][1] >= top5[i+1][1]
    
    def test_get_edge_weight_returns_count(self, graph):
        """Test get edge weight"""
        # 'whole milk' and 'other vegetables' should co-occur many times
        weight = graph.get_edge_weight('whole milk', 'other vegetables')
        
        assert weight > 0
        assert isinstance(weight, int)
    
    def test_get_edge_weight_nonexistent_returns_zero(self, graph):
        """Test non-existent edge returns 0"""
        weight = graph.get_edge_weight('nonexistent1', 'nonexistent2')
        assert weight == 0
    
    def test_get_top_neighbors_k_exceeds_available(self, graph):
        """Test when k is larger than available neighbors"""
        # Request more neighbors than exist
        neighbors = graph.get_top_neighbors('whole milk', top_k=1000)
        
        # Should return all available neighbors (not crash)
        assert isinstance(neighbors, list)
        assert len(neighbors) <= 1000
    
    def test_edge_symmetry(self, graph):
        """Test that edge(A,B) == edge(B,A) (undirected graph)"""
        weight_ab = graph.get_edge_weight('whole milk', 'other vegetables')
        weight_ba = graph.get_edge_weight('other vegetables', 'whole milk')
        
        assert weight_ab == weight_ba
        assert weight_ab > 0


class TestAddTransaction:
    """Test dynamic transaction addition (new feature)"""
    
    @pytest.fixture
    def empty_graph(self):
        """Create empty graph for testing add_transaction"""
        return GraphAdjacencyList()
    
    def test_add_transaction_creates_edges(self, empty_graph):
        """Test adding transaction creates edges"""
        empty_graph.add_transaction(['milk', 'bread', 'eggs'])
        
        # Verify items exist
        assert empty_graph.has_item('milk')
        assert empty_graph.has_item('bread')
        assert empty_graph.has_item('eggs')
        
        # Verify edges exist
        assert empty_graph.get_edge_weight('milk', 'bread') == 1
        assert empty_graph.get_edge_weight('milk', 'eggs') == 1
        assert empty_graph.get_edge_weight('bread', 'eggs') == 1
    
    def test_add_transaction_increments_existing_edges(self, empty_graph):
        """Test repeated additions increment weight"""
        empty_graph.add_transaction(['milk', 'bread'])
        empty_graph.add_transaction(['milk', 'bread'])
        
        # Weight should be 2
        assert empty_graph.get_edge_weight('milk', 'bread') == 2
    
    def test_add_transaction_handles_duplicates_in_basket(self, empty_graph):
        """Test deduplication within basket"""
        empty_graph.add_transaction(['milk', 'milk', 'bread'])
        
        # Should count co-occurrence only once
        assert empty_graph.get_edge_weight('milk', 'bread') == 1
    
    def test_add_transaction_single_item_no_edges(self, empty_graph):
        """Test single item creates no edges"""
        empty_graph.add_transaction(['milk'])
        
        assert empty_graph.has_item('milk')
        neighbors = empty_graph.get_neighbors('milk')
        assert len(neighbors) == 0
    
    def test_add_transaction_updates_item_list(self, empty_graph):
        """Test adding new items updates item list"""
        empty_graph.add_transaction(['item1', 'item2'])
        
        items = empty_graph.get_all_items()
        assert 'item1' in items
        assert 'item2' in items
    
    def test_add_transaction_empty_list(self, empty_graph):
        """Test adding empty transaction"""
        empty_graph.add_transaction([])
        
        # Should not crash, no items added
        assert len(empty_graph.get_all_items()) == 0
    
    def test_add_transaction_large_basket(self, empty_graph):
        """Test handling basket with many items (stress test)"""
        large_basket = [f'item{i}' for i in range(50)]
        empty_graph.add_transaction(large_basket)
        
        # Should create all items
        assert len(empty_graph.get_all_items()) == 50
        # Should create edges (50 choose 2 = 1225 edges)
        assert empty_graph.get_edge_weight('item0', 'item49') == 1
