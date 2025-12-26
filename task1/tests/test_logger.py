"""
Minimal test for logging functionality (TDD RED phase).

Following TDD: Write minimal tests to define core behavior.
"""

import os
import sys
import pytest
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


class TestLogger:
    """Minimal test suite for activity logger."""
    
    def setup_method(self):
        """Setup test environment."""
        self.test_log_dir = "task1/logs/test"
        self.test_log_file = os.path.join(self.test_log_dir, "test_activity.log")
        
        # Clean up test log file if exists
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)
    
    def teardown_method(self):
        """Clean up after test."""
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)
    
    def test_logger_basic_functionality(self):
        """Test core logging functionality."""
        from task1.logger import ActivityLogger
        
        logger = ActivityLogger(log_dir=self.test_log_dir)
        
        # Test logger creation
        assert logger is not None
        assert os.path.exists(self.test_log_dir)
        
        # Test logging operations
        logger.log_crud("CREATE", "Added record for China 2020")
        logger.log_cleaning("PIPELINE", "Cleaned 100 records")
        logger.log_filter("country", "China")
        logger.log_export("CSV", "output.csv", 150)
        
        # Verify log file exists and has content
        assert os.path.exists(self.test_log_file)
        
        with open(self.test_log_file, 'r') as f:
            content = f.read()
            
            # Verify all operations are logged with timestamp
            assert datetime.now().strftime("%Y-%m-%d") in content
            assert "CREATE" in content
            assert "CLEANING" in content
            assert "FILTER" in content
            assert "EXPORT" in content
            assert "China" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
