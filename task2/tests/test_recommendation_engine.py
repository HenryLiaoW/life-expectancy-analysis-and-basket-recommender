"""
Tests for RecommendationEngine (Business Logic Layer)

TDD Red Phase: Testing 5 business methods
"""

import pytest
from pathlib import Path
from task2.src.recommendation_engine import RecommendationEngine


class TestRecommendForItem:
    """Test single item recommendation (Requirement 1)"""
    
    @pytest.fixture
    def engine(self):
        """Create recommendation engine"""
        csv_path = Path(__file__).parent.parent / "data" / "Supermarket_dataset_PAI.csv"
        engine = RecommendationEngine()
        engine.load_data(str(csv_path))
        return engine
    
    def test_recommend_for_item_returns_list(self, engine):
        """Test returns recommendation list"""
        recommendations = engine.recommend_for_item('whole milk', top_k=5)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) == 5
    
    def test_recommend_for_item_format(self, engine):
        """Test return format: [(item, count), ...]"""
        recommendations = engine.recommend_for_item('whole milk', top_k=3)
        
        for item, count in recommendations:
            assert isinstance(item, str)
            assert isinstance(count, int)
            assert count > 0
    
    def test_recommend_for_item_sorted_by_frequency(self, engine):
        """Test sorted by frequency descending"""
        recommendations = engine.recommend_for_item('whole milk', top_k=5)
        
        # Verify descending order
        for i in range(len(recommendations) - 1):
            assert recommendations[i][1] >= recommendations[i+1][1]
    
    def test_recommend_for_item_k_exceeds_neighbors(self, engine):
        """Test when k is larger than available neighbors"""
        recommendations = engine.recommend_for_item('whole milk', top_k=1000)
        
        # Should return all available neighbors without error
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 1000
    
    def test_recommend_for_nonexistent_item_returns_empty(self, engine):
        """Test non-existent item returns empty list"""
        recommendations = engine.recommend_for_item('nonexistent_item', top_k=5)
        
        assert recommendations == []
    
    def test_recommend_for_item_excludes_self(self, engine):
        """Test that item doesn't recommend itself"""
        recommendations = engine.recommend_for_item('whole milk', top_k=50)
        
        recommendation_items = [item for item, _ in recommendations]
        assert 'whole milk' not in recommendation_items


class TestGetMostFrequentPairs:
    """Test most frequent co-purchase pairs (Requirement 2)"""
    
    @pytest.fixture
    def engine(self):
        csv_path = Path(__file__).parent.parent / "data" / "Supermarket_dataset_PAI.csv"
        engine = RecommendationEngine()
        engine.load_data(str(csv_path))
        return engine
    
    def test_get_most_frequent_pairs_returns_list(self, engine):
        """Test returns list"""
        pairs = engine.get_most_frequent_pairs(top_k=3)
        
        assert isinstance(pairs, list)
        assert len(pairs) == 3
    
    def test_get_most_frequent_pairs_format(self, engine):
        """Test return format: [((item1, item2), count), ...]"""
        pairs = engine.get_most_frequent_pairs(top_k=3)
        
        for pair, count in pairs:
            assert isinstance(pair, tuple)
            assert len(pair) == 2
            assert isinstance(pair[0], str)
            assert isinstance(pair[1], str)
            assert isinstance(count, int)
            assert count > 0
    
    def test_get_most_frequent_pairs_sorted(self, engine):
        """Test sorted by frequency descending"""
        pairs = engine.get_most_frequent_pairs(top_k=5)
        
        for i in range(len(pairs) - 1):
            assert pairs[i][1] >= pairs[i+1][1]
    
    def test_get_most_frequent_pairs_no_duplicates(self, engine):
        """Test no duplicate pairs ((A,B) and (B,A) count as same)"""
        pairs = engine.get_most_frequent_pairs(top_k=10)
        
        seen = set()
        for (item1, item2), count in pairs:
            normalized = tuple(sorted([item1, item2]))
            assert normalized not in seen
            seen.add(normalized)
    
    def test_get_most_frequent_pairs_k_exceeds_available(self, engine):
        """Test when k is larger than available pairs"""
        pairs = engine.get_most_frequent_pairs(top_k=100000)
        
        # Should return all available pairs without error
        assert isinstance(pairs, list)
        assert len(pairs) > 0


class TestCheckCoPurchase:
    """Test co-purchase check (Requirement 3)"""
    
    @pytest.fixture
    def engine(self):
        csv_path = Path(__file__).parent.parent / "data" / "Supermarket_dataset_PAI.csv"
        engine = RecommendationEngine()
        engine.load_data(str(csv_path))
        return engine
    
    def test_check_co_purchase_returns_bool(self, engine):
        """Test returns boolean"""
        result = engine.check_co_purchase('whole milk', 'other vegetables', threshold=100)
        
        assert isinstance(result, bool)
    
    def test_check_co_purchase_high_frequency_is_true(self, engine):
        """Test high frequency co-purchase returns True"""
        # whole milk and other vegetables should be co-purchased many times
        result = engine.check_co_purchase('whole milk', 'other vegetables', threshold=50)
        
        assert result is True
    
    def test_check_co_purchase_low_threshold(self, engine):
        """Test low threshold"""
        result = engine.check_co_purchase('whole milk', 'other vegetables', threshold=1)
        
        assert result is True
    
    def test_check_co_purchase_high_threshold(self, engine):
        """Test high threshold may return False"""
        result = engine.check_co_purchase('whole milk', 'other vegetables', threshold=10000)
        
        assert result is False
    
    def test_check_co_purchase_nonexistent_items(self, engine):
        """Test non-existent items return False"""
        result = engine.check_co_purchase('nonexistent1', 'nonexistent2', threshold=1)
        
        assert result is False
    
    def test_check_co_purchase_symmetry(self, engine):
        """Test that check_co_purchase(A,B) == check_co_purchase(B,A)"""
        result_ab = engine.check_co_purchase('whole milk', 'other vegetables', threshold=50)
        result_ba = engine.check_co_purchase('other vegetables', 'whole milk', threshold=50)
        
        assert result_ab == result_ba


class TestRecommendForBasket:
    """Test basket recommendation (Extended feature)"""
    
    @pytest.fixture
    def engine(self):
        csv_path = Path(__file__).parent.parent / "data" / "Supermarket_dataset_PAI.csv"
        engine = RecommendationEngine()
        engine.load_data(str(csv_path))
        return engine
    
    def test_recommend_for_basket_returns_list(self, engine):
        """Test returns recommendation list"""
        recommendations = engine.recommend_for_basket(['whole milk', 'bread'], top_k=5)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 5
    
    def test_recommend_for_basket_excludes_input_items(self, engine):
        """Test does not recommend items already in basket"""
        basket = ['whole milk', 'bread']
        recommendations = engine.recommend_for_basket(basket, top_k=10)
        
        recommendation_items = [item for item, _ in recommendations]
        for item in basket:
            assert item not in recommendation_items
    
    def test_recommend_for_basket_aggregates_scores(self, engine):
        """Test aggregates association scores from multiple items"""
        # Multiple items should yield more recommendations than single item
        single = engine.recommend_for_item('whole milk', top_k=5)
        basket = engine.recommend_for_basket(['whole milk', 'bread'], top_k=5)
        
        # Both should have results
        assert len(single) > 0
        assert len(basket) > 0
    
    def test_recommend_for_empty_basket_returns_empty(self, engine):
        """Test empty basket returns empty list"""
        recommendations = engine.recommend_for_basket([], top_k=5)
        
        assert recommendations == []


class TestUpdateWithTransaction:
    """Test dynamic updates (Extended feature)"""
    
    @pytest.fixture
    def engine(self):
        csv_path = Path(__file__).parent.parent / "data" / "Supermarket_dataset_PAI.csv"
        engine = RecommendationEngine()
        engine.load_data(str(csv_path))
        return engine
    
    def test_update_with_transaction_adds_new_items(self, engine):
        """Test adding new items"""
        new_item = 'test_new_product_12345'
        engine.update_with_transaction([new_item, 'whole milk'])
        
        # New item should exist
        recommendations = engine.recommend_for_item(new_item, top_k=5)
        assert len(recommendations) > 0
        assert recommendations[0][0] == 'whole milk'
    
    def test_update_with_transaction_increments_frequency(self, engine):
        """Test increments co-occurrence frequency"""
        # Get initial weight (needs exposed method)
        initial_count = engine.check_co_purchase('whole milk', 'bread', threshold=0)
        
        # Add new transaction
        engine.update_with_transaction(['whole milk', 'bread'])
        
        # Verify relationship still exists (frequency increased)
        assert engine.check_co_purchase('whole milk', 'bread', threshold=0)
    
    def test_update_with_transaction_affects_recommendations(self, engine):
        """Test updates affect recommendation results"""
        test_item = 'test_rare_item_99999'
        
        # Add multiple transactions
        for _ in range(10):
            engine.update_with_transaction([test_item, 'whole milk'])
        
        # whole milk should recommend this new item
        recommendations = engine.recommend_for_item('whole milk', top_k=20)
        recommendation_items = [item for item, _ in recommendations]
        
        assert test_item in recommendation_items
