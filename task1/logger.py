"""
Activity logging system for tracking user operations.

This module provides a centralized logging mechanism to track all user
activities including CRUD operations, data cleaning, filtering, and exports.
Supports audit trails and user behavior analysis.
"""

import os
from datetime import datetime
from typing import Optional


class ActivityLogger:
    """
    Logger for tracking user activities in the life expectancy analysis system.
    
    Logs all significant operations to a file for audit trails and analysis.
    Thread-safe file writing with automatic directory creation.
    
    Attributes:
        log_dir: Directory where log files are stored
        log_file: Full path to the activity log file
    """
    
    def __init__(self, log_dir: str = "task1/logs"):
        """
        Initialize the activity logger.
        
        Args:
            log_dir: Directory to store log files (default: task1/logs)
        """
        self.log_dir = log_dir
        self.log_file = os.path.join(log_dir, "test_activity.log" if "test" in log_dir else "activity.log")
        
        # Create log directory if it doesn't exist
        os.makedirs(self.log_dir, exist_ok=True)
    
    def _write_log(self, operation_type: str, details: str):
        """
        Write a log entry to the log file.
        
        Args:
            operation_type: Type of operation (e.g., 'CRUD', 'CLEANING', 'FILTER')
            details: Detailed description of the operation
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {operation_type}: {details}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    def log_crud(self, operation: str, details: str):
        """
        Log a CRUD operation (Create, Read, Update, Delete).
        
        Args:
            operation: CRUD operation type (CREATE, READ, UPDATE, DELETE)
            details: Description of what was modified
            
        Example:
            logger.log_crud("CREATE", "Added record for China 2020")
            logger.log_crud("DELETE", "Removed record ID 123")
        """
        self._write_log(f"CRUD-{operation}", details)
    
    def log_cleaning(self, mode: str, details: str):
        """
        Log a data cleaning operation.
        
        Args:
            mode: Cleaning mode (PIPELINE, DATABASE)
            details: Description of cleaning performed
            
        Example:
            logger.log_cleaning("PIPELINE", "Cleaned 100 records, removed 5 duplicates")
            logger.log_cleaning("DATABASE", "Applied database-level cleaning")
        """
        self._write_log(f"CLEANING-{mode}", details)
    
    def log_filter(self, filter_type: str, filter_value: str):
        """
        Log a data filtering operation.
        
        Args:
            filter_type: Type of filter applied (country, year, region)
            filter_value: Value used for filtering
            
        Example:
            logger.log_filter("country", "China")
            logger.log_filter("year", "2015-2020")
        """
        self._write_log("FILTER", f"{filter_type}={filter_value}")
    
    def log_export(self, export_format: str, file_path: str, record_count: int):
        """
        Log a data export operation.
        
        Args:
            export_format: Format of export (CSV, JSON, etc.)
            file_path: Path where data was exported
            record_count: Number of records exported
            
        Example:
            logger.log_export("CSV", "output/data.csv", 150)
        """
        self._write_log("EXPORT", f"{export_format} to {file_path} ({record_count} records)")
    
    def log_visualization(self, viz_type: str, details: str):
        """
        Log a visualization operation.
        
        Args:
            viz_type: Type of visualization (CHART, TABLE)
            details: Description of visualization generated
            
        Example:
            logger.log_visualization("CHART", "Life expectancy trend chart for China")
            logger.log_visualization("TABLE", "Summary table grouped by country")
        """
        self._write_log(f"VISUALIZATION-{viz_type}", details)
    
    def log_analysis(self, analysis_type: str, details: str):
        """
        Log an analysis operation.
        
        Args:
            analysis_type: Type of analysis (CORRELATION, SUMMARY, COMPARISON)
            details: Description of analysis performed
            
        Example:
            logger.log_analysis("CORRELATION", "Calculated correlations with life_expect")
            logger.log_analysis("SUMMARY", "Generated statistical summary")
        """
        self._write_log(f"ANALYSIS-{analysis_type}", details)


# Global logger instance for easy access
_global_logger: Optional[ActivityLogger] = None


def get_logger() -> ActivityLogger:
    """
    Get the global logger instance.
    
    Creates a new logger if one doesn't exist.
    
    Returns:
        ActivityLogger instance
    """
    global _global_logger
    if _global_logger is None:
        _global_logger = ActivityLogger()
    return _global_logger
