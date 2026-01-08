"""
Test suite for development status filtering functionality.

This test suite follows TDD (Test-Driven Development) principles and covers:
- Single status filtering (high, upper-middle, lower-middle, low)
- Multiple status filtering (combinations)
- Edge cases and boundary values
- Invalid input handling
- Data validation and robustness

Tests are written BEFORE implementation to ensure requirements are met.
"""

import pytest
import pandas as pd
import numpy as np
from task1.src.data_filter import filter_by_development_status


@pytest.fixture
def sample_data():
    """Create sample life expectancy data with various GNI levels."""
    return pd.DataFrame({
        'country': [
            'USA', 'USA', 'USA',
            'China', 'China', 'China',
            'India', 'India', 'India',
            'Somalia', 'Somalia', 'Somalia',
            'Brunei', 'Brunei', 'Brunei',
        ],
        'year': [2000, 2001, 2002] * 5,
        'life_expectancy': [75, 76, 77] * 5,
        'gni_capita': [
            45000, 46000, 47000,  # USA - High income
            5000, 5500, 6000,      # China - Upper middle
            2000, 2100, 2200,      # India - Lower middle
            500, 550, 600,         # Somalia - Low income
            65000, 66000, 67000,   # Brunei - High income
        ]
    })


@pytest.fixture
def edge_case_data():
    """Create data with exact threshold boundaries."""
    return pd.DataFrame({
        'country': [
            'Threshold_High', 'Threshold_UpperMid', 
            'Threshold_LowerMid', 'Threshold_Low'
        ],
        'year': [2010] * 4,
        'life_expectancy': [75, 72, 68, 60],
        'gni_capita': [
            14006,  # Exactly at high income threshold
            4516,   # Exactly at upper-middle threshold
            1146,   # Exactly at lower-middle threshold
            1145,   # Exactly at low income upper bound
        ]
    })


class TestSingleStatusFiltering:
    """Test filtering with single development status."""
    
    def test_filter_high_income(self, sample_data):
        """Test filtering high income countries (GNI >= $14,006)."""
        result = filter_by_development_status(sample_data, 'high')
        
        assert len(result) == 6  # USA (3) + Brunei (3)
        assert set(result['country'].unique()) == {'USA', 'Brunei'}
        assert all(result['gni_capita'] >= 14006)
    
    def test_filter_upper_middle_income(self, sample_data):
        """Test filtering upper-middle income countries ($4,516-$14,005)."""
        result = filter_by_development_status(sample_data, 'upper-middle')
        
        assert len(result) == 3  # China (3)
        assert result['country'].unique()[0] == 'China'
        assert all((result['gni_capita'] >= 4516) & (result['gni_capita'] <= 14005))
    
    def test_filter_lower_middle_income(self, sample_data):
        """Test filtering lower-middle income countries ($1,146-$4,515)."""
        result = filter_by_development_status(sample_data, 'lower-middle')
        
        assert len(result) == 3  # India (3)
        assert result['country'].unique()[0] == 'India'
        assert all((result['gni_capita'] >= 1146) & (result['gni_capita'] <= 4515))
    
    def test_filter_low_income(self, sample_data):
        """Test filtering low income countries (GNI <= $1,145)."""
        result = filter_by_development_status(sample_data, 'low')
        
        assert len(result) == 3  # Somalia (3)
        assert result['country'].unique()[0] == 'Somalia'
        assert all(result['gni_capita'] <= 1145)


class TestMultipleStatusFiltering:
    """Test filtering with multiple development statuses."""
    
    def test_filter_two_statuses(self, sample_data):
        """Test filtering with two income classifications."""
        result = filter_by_development_status(sample_data, ['high', 'upper-middle'])
        
        assert len(result) == 9  # USA (3) + Brunei (3) + China (3)
        assert set(result['country'].unique()) == {'USA', 'Brunei', 'China'}
    
    def test_filter_three_statuses(self, sample_data):
        """Test filtering with three income classifications."""
        result = filter_by_development_status(sample_data, ['high', 'upper-middle', 'lower-middle'])
        
        assert len(result) == 12  # USA + Brunei + China + India
        assert set(result['country'].unique()) == {'USA', 'Brunei', 'China', 'India'}
    
    def test_filter_all_four_statuses(self, sample_data):
        """Test filtering with all income classifications (should return all data)."""
        result = filter_by_development_status(
            sample_data, 
            ['high', 'upper-middle', 'lower-middle', 'low']
        )
        
        assert len(result) == len(sample_data)
        assert set(result['country'].unique()) == set(sample_data['country'].unique())
    
    def test_filter_non_adjacent_statuses(self, sample_data):
        """Test filtering with non-adjacent classifications (high + low)."""
        result = filter_by_development_status(sample_data, ['high', 'low'])
        
        assert len(result) == 9  # USA (3) + Brunei (3) + Somalia (3)
        assert set(result['country'].unique()) == {'USA', 'Brunei', 'Somalia'}
    
    def test_filter_duplicate_statuses(self, sample_data):
        """Test that duplicate statuses don't cause issues."""
        result = filter_by_development_status(sample_data, ['high', 'high', 'upper-middle'])
        
        # Should be same as ['high', 'upper-middle']
        assert len(result) == 9
        assert set(result['country'].unique()) == {'USA', 'Brunei', 'China'}


class TestBoundaryValues:
    """Test exact threshold boundaries."""
    
    def test_exact_high_income_threshold(self, edge_case_data):
        """Test country exactly at $14,006 is classified as high income."""
        result = filter_by_development_status(edge_case_data, 'high')
        
        assert len(result) == 1
        assert result.iloc[0]['country'] == 'Threshold_High'
        assert result.iloc[0]['gni_capita'] == 14006
    
    def test_exact_upper_middle_threshold(self, edge_case_data):
        """Test country exactly at $4,516 is classified as upper-middle."""
        result = filter_by_development_status(edge_case_data, 'upper-middle')
        
        assert len(result) == 1
        assert result.iloc[0]['country'] == 'Threshold_UpperMid'
        assert result.iloc[0]['gni_capita'] == 4516
    
    def test_exact_lower_middle_threshold(self, edge_case_data):
        """Test country exactly at $1,146 is classified as lower-middle."""
        result = filter_by_development_status(edge_case_data, 'lower-middle')
        
        assert len(result) == 1
        assert result.iloc[0]['country'] == 'Threshold_LowerMid'
        assert result.iloc[0]['gni_capita'] == 1146
    
    def test_exact_low_income_upper_bound(self, edge_case_data):
        """Test country exactly at $1,145 is classified as low income."""
        result = filter_by_development_status(edge_case_data, 'low')
        
        assert len(result) == 1
        assert result.iloc[0]['country'] == 'Threshold_Low'
        assert result.iloc[0]['gni_capita'] == 1145
    
    def test_boundary_coverage_complete(self, edge_case_data):
        """Test all thresholds together cover entire range."""
        all_statuses = ['high', 'upper-middle', 'lower-middle', 'low']
        result = filter_by_development_status(edge_case_data, all_statuses)
        
        assert len(result) == 4  # All threshold countries included
        assert set(result['country'].unique()) == set(edge_case_data['country'].unique())


class TestInvalidInputHandling:
    """Test error handling and robustness."""
    
    def test_invalid_status_string(self, sample_data):
        """Test that invalid status raises ValueError."""
        with pytest.raises(ValueError, match="Status must be one of"):
            filter_by_development_status(sample_data, 'invalid-status')
    
    def test_invalid_status_in_list(self, sample_data):
        """Test that invalid status in list raises ValueError."""
        with pytest.raises(ValueError, match="Status must be one of"):
            filter_by_development_status(sample_data, ['high', 'invalid', 'low'])
    
    def test_empty_status_list(self, sample_data):
        """Test that empty list is handled gracefully."""
        # Empty list should return empty DataFrame (no matches)
        result = filter_by_development_status(sample_data, [])
        assert len(result) == 0
    
    def test_missing_gni_column(self):
        """Test that missing gni_capita column raises ValueError."""
        df_no_gni = pd.DataFrame({
            'country': ['USA', 'China'],
            'year': [2000, 2000],
            'life_expectancy': [75, 73]
        })
        
        with pytest.raises(ValueError, match="must have 'gni_capita' column"):
            filter_by_development_status(df_no_gni, 'high')
    
    def test_case_sensitivity(self, sample_data):
        """Test that status parameter is case-sensitive (should fail with uppercase)."""
        with pytest.raises(ValueError):
            filter_by_development_status(sample_data, 'High')
    
    def test_typo_in_status(self, sample_data):
        """Test common typos are caught."""
        with pytest.raises(ValueError):
            filter_by_development_status(sample_data, 'upper middle')  # Missing hyphen


class TestDataIntegrity:
    """Test that filtering preserves data integrity."""
    
    def test_original_data_unchanged(self, sample_data):
        """Test that filtering doesn't modify original DataFrame."""
        original_len = len(sample_data)
        original_countries = set(sample_data['country'].unique())
        
        _ = filter_by_development_status(sample_data, 'high')
        
        assert len(sample_data) == original_len
        assert set(sample_data['country'].unique()) == original_countries
    
    def test_filtered_data_is_copy(self, sample_data):
        """Test that filtered data is a copy, not a view."""
        result = filter_by_development_status(sample_data, 'high')
        
        # Modify result
        result.loc[result.index[0], 'life_expectancy'] = 999
        
        # Original should be unchanged
        assert not any(sample_data['life_expectancy'] == 999)
    
    def test_all_columns_preserved(self, sample_data):
        """Test that all columns are preserved in filtered data."""
        result = filter_by_development_status(sample_data, 'high')
        
        assert list(result.columns) == list(sample_data.columns)
    
    def test_index_preserved(self, sample_data):
        """Test that DataFrame index is preserved."""
        result = filter_by_development_status(sample_data, 'high')
        
        # Result indices should be subset of original indices
        assert all(idx in sample_data.index for idx in result.index)


class TestEmptyAndSpecialCases:
    """Test edge cases with empty or special data."""
    
    def test_empty_dataframe(self):
        """Test filtering on empty DataFrame."""
        empty_df = pd.DataFrame(columns=['country', 'year', 'life_expectancy', 'gni_capita'])
        result = filter_by_development_status(empty_df, 'high')
        
        assert len(result) == 0
        assert list(result.columns) == list(empty_df.columns)
    
    def test_no_matches(self, sample_data):
        """Test when no data matches filter criteria."""
        # Filter for low income in data with only high/middle income
        high_income_only = sample_data[sample_data['gni_capita'] > 2000]
        result = filter_by_development_status(high_income_only, 'low')
        
        assert len(result) == 0
    
    def test_nan_gni_values(self):
        """Test handling of NaN GNI values."""
        df_with_nan = pd.DataFrame({
            'country': ['USA', 'Unknown', 'China'],
            'year': [2000, 2000, 2000],
            'life_expectancy': [75, 70, 73],
            'gni_capita': [45000, np.nan, 5000]
        })
        
        result = filter_by_development_status(df_with_nan, 'high')
        
        # NaN should not match any filter
        assert len(result) == 1
        assert result.iloc[0]['country'] == 'USA'
    
    def test_zero_gni_value(self):
        """Test handling of zero GNI (should be low income)."""
        df_with_zero = pd.DataFrame({
            'country': ['NoData'],
            'year': [2000],
            'life_expectancy': [50],
            'gni_capita': [0]
        })
        
        result = filter_by_development_status(df_with_zero, 'low')
        assert len(result) == 1
    
    def test_negative_gni_value(self):
        """Test handling of negative GNI (edge case, shouldn't match low income by threshold)."""
        df_with_negative = pd.DataFrame({
            'country': ['Negative'],
            'year': [2000],
            'life_expectancy': [50],
            'gni_capita': [-100]
        })
        
        # Negative GNI doesn't match low income threshold (0-1145)
        result = filter_by_development_status(df_with_negative, 'low')
        assert len(result) == 0


class TestRealWorldScenarios:
    """Test realistic scenarios from actual usage."""
    
    def test_developed_and_developing_countries(self, sample_data):
        """Test common use case: comparing developed vs developing."""
        developed = filter_by_development_status(sample_data, 'high')
        developing = filter_by_development_status(
            sample_data, 
            ['upper-middle', 'lower-middle', 'low']
        )
        
        # Should partition all data
        assert len(developed) + len(developing) == len(sample_data)
        
        # No overlap
        developed_countries = set(developed['country'].unique())
        developing_countries = set(developing['country'].unique())
        assert len(developed_countries & developing_countries) == 0
    
    def test_middle_income_trap_analysis(self, sample_data):
        """Test analyzing middle-income countries."""
        middle_income = filter_by_development_status(
            sample_data,
            ['upper-middle', 'lower-middle']
        )
        
        assert len(middle_income) == 6  # China + India
        assert set(middle_income['country'].unique()) == {'China', 'India'}
    
    def test_extreme_poverty_analysis(self, sample_data):
        """Test identifying countries in extreme poverty."""
        low_income = filter_by_development_status(sample_data, 'low')
        
        assert all(low_income['gni_capita'] <= 1145)
        assert 'Somalia' in low_income['country'].values
