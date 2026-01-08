"""
Test suite for main_cli.py - Main Entry Point Testing

This module tests the main entry point and routing logic of the
Life Expectancy Data Insights System.

Following TDD principles:
- Test core functions (print_welcome, print_main_menu)
- Test routing logic (run_data_analysis, run_crud_operations)
- Test database path validation
- Test user interaction flows

Author: Suhang Liao
Module: Programming for Artificial Intelligence WM9QF-15
"""

import pytest
import os
import sys
from io import StringIO
from unittest.mock import patch, MagicMock

# Import the module to be tested
from task1.main import (
    print_welcome,
    print_main_menu,
    run_data_analysis,
    run_crud_operations,
    run_create_database
)


class TestPrintFunctions:
    """Test suite for output/display functions."""
    
    def test_print_welcome_output(self, capsys):
        """Test welcome banner prints correctly."""
        print_welcome()
        captured = capsys.readouterr()
        
        # Check key components are present
        assert "Life Expectancy Data Insights System" in captured.out
        assert "WHO Public Health Data Analysis & Management" in captured.out
        assert "=" in captured.out  # Banner borders
    
    def test_print_welcome_has_separators(self, capsys):
        """Test welcome banner has proper formatting."""
        print_welcome()
        captured = capsys.readouterr()
        
        # Should have multiple separator lines
        lines = captured.out.split('\n')
        separator_count = sum(1 for line in lines if '=' in line and len(line) > 50)
        assert separator_count >= 3, "Should have at least 3 separator lines"
    
    def test_print_main_menu_shows_all_options(self, capsys):
        """Test main menu displays all required options."""
        print_main_menu()
        captured = capsys.readouterr()
        
        # Check all menu options are present
        assert "1 - Data Analysis Pipeline" in captured.out
        assert "2 - Database CRUD Operations" in captured.out
        assert "3 - Create Database from CSV" in captured.out
        assert "0 - Exit" in captured.out
    
    def test_print_main_menu_has_descriptions(self, capsys):
        """Test menu includes helpful descriptions."""
        print_main_menu()
        captured = capsys.readouterr()
        
        # Check descriptions are present
        assert "Filter, Clean, Analyze, Visualize" in captured.out
        assert "Create, Read, Update, Delete" in captured.out
        assert "Convert CSV file to SQLite database" in captured.out
    
    def test_print_main_menu_format(self, capsys):
        """Test menu has proper formatting."""
        print_main_menu()
        captured = capsys.readouterr()
        
        # Should have "Main Menu" header
        assert "Main Menu" in captured.out
        # Should have emoji or formatting
        assert "📋" in captured.out or "Main Menu:" in captured.out


class TestDataAnalysisRouting:
    """Test suite for data analysis pipeline routing."""
    
    @patch('task1.src.menu_cli.run_menu_system')
    def test_run_data_analysis_calls_menu_system(self, mock_menu, capsys):
        """Test that run_data_analysis calls the menu system."""
        test_db = "test.db"
        
        run_data_analysis(test_db)
        
        # Verify menu_system was called with correct database path
        mock_menu.assert_called_once_with(test_db)
        
        # Check output message
        captured = capsys.readouterr()
        assert "Launching Data Analysis Pipeline" in captured.out
    
    @patch('task1.src.menu_cli.run_menu_system')
    def test_run_data_analysis_with_different_paths(self, mock_menu):
        """Test data analysis routing with various database paths."""
        test_paths = [
            "task1/data/CLI_demo.db",
            "task1/data/test_life_expectancy.db",
            "/absolute/path/to/database.db"
        ]
        
        for path in test_paths:
            mock_menu.reset_mock()
            run_data_analysis(path)
            mock_menu.assert_called_once_with(path)
    
    @patch('task1.src.menu_cli.run_menu_system')
    def test_run_data_analysis_prints_header(self, mock_menu, capsys):
        """Test that data analysis prints a proper header."""
        run_data_analysis("test.db")
        captured = capsys.readouterr()
        
        # Should have separator lines
        assert "=" in captured.out
        # Should have launching message
        assert "Launching" in captured.out or "Data Analysis" in captured.out


class TestCRUDOperationsRouting:
    """Test suite for CRUD operations routing."""
    
    @patch('builtins.input', side_effect=['back'])
    @patch('task1.src.database_loader.get_all_records')
    def test_run_crud_operations_exits_on_back(self, mock_records, mock_input, capsys):
        """Test CRUD interface exits when user types 'back'."""
        test_db = "test.db"
        
        run_crud_operations(test_db)
        
        captured = capsys.readouterr()
        # Should show CRUD launch message
        assert "CRUD Operations" in captured.out or "Launching" in captured.out
        # Should show return message
        assert "Returning" in captured.out or "main menu" in captured.out
    
    @patch('builtins.input', side_effect=['help', 'back'])
    @patch('task1.src.database_loader.get_all_records')
    def test_run_crud_operations_shows_help(self, mock_records, mock_input, capsys):
        """Test CRUD help command displays available commands."""
        run_crud_operations("test.db")
        
        captured = capsys.readouterr()
        # Check help output contains key commands
        output_lower = captured.out.lower()
        assert 'create' in output_lower
        assert 'read' in output_lower
        assert 'update' in output_lower
        assert 'delete' in output_lower
        assert 'list' in output_lower
    
    @patch('builtins.input', side_effect=['list', 'back'])
    @patch('task1.src.database_loader.get_all_records')
    def test_run_crud_operations_list_command(self, mock_records, mock_input, capsys):
        """Test CRUD list command displays records."""
        # Mock database records
        mock_records.return_value = [
            {'country': 'China', 'year': 2015, 'life_expect': 76.1},
            {'country': 'China', 'year': 2016, 'life_expect': 76.4},
            {'country': 'India', 'year': 2015, 'life_expect': 68.3},
        ]
        
        run_crud_operations("test.db")
        
        captured = capsys.readouterr()
        # Should show total records
        assert 'Total records' in captured.out or '3' in captured.out
        # Should call get_all_records
        mock_records.assert_called()
    
    @patch('builtins.input', side_effect=['invalid_command', 'back'])
    @patch('task1.src.database_loader.get_all_records')
    def test_run_crud_operations_handles_invalid_command(self, mock_records, mock_input, capsys):
        """Test CRUD interface handles invalid commands gracefully."""
        run_crud_operations("test.db")
        
        captured = capsys.readouterr()
        # Should show error or unknown command message
        assert 'Unknown' in captured.out or 'Invalid' in captured.out or 'help' in captured.out


class TestDatabaseCreation:
    """Test suite for database creation functionality."""
    
    @patch('builtins.input', side_effect=['1', '', 'no'])
    @patch('os.path.exists', return_value=True)
    def test_run_create_database_cancels_on_existing(self, mock_exists, mock_input, capsys):
        """Test database creation cancels when file exists and user says no."""
        run_create_database()
        
        captured = capsys.readouterr()
        # Should show cancelled message
        assert 'Cancelled' in captured.out or 'cancelled' in captured.out
    
    @patch('builtins.input', side_effect=['3', '', 'yes'])
    @patch('os.path.exists', return_value=False)
    @patch('task1.src.create_db.create_db_from_csv')
    def test_run_create_database_demo_option(self, mock_create, mock_exists, mock_input, capsys):
        """Test database creation with demo data option."""
        mock_create.return_value = "task1/data/CLI_demo.db"
        
        run_create_database()
        
        # Should call create function
        mock_create.assert_called()
        
        captured = capsys.readouterr()
        # Should show success message
        assert 'successfully' in captured.out or 'created' in captured.out
    
    @patch('builtins.input', side_effect=['5'])  # Invalid choice
    def test_run_create_database_handles_invalid_choice(self, mock_input, capsys):
        """Test database creation handles invalid menu choice."""
        run_create_database()
        
        captured = capsys.readouterr()
        # Should show invalid choice message
        assert 'Invalid' in captured.out or 'invalid' in captured.out


class TestEdgeCases:
    """Test suite for edge cases and error handling."""
    
    def test_print_functions_do_not_crash(self):
        """Test that print functions execute without exceptions."""
        # These should never raise exceptions
        try:
            print_welcome()
            print_main_menu()
        except Exception as e:
            pytest.fail(f"Print functions should not raise exceptions: {e}")
    
    @patch('task1.src.menu_cli.run_menu_system', side_effect=Exception("Test error"))
    def test_run_data_analysis_handles_menu_errors(self, mock_menu):
        """Test that data analysis handles errors from menu system."""
        # Should not crash even if menu_system raises exception
        try:
            with pytest.raises(Exception, match="Test error"):
                run_data_analysis("test.db")
        except Exception as e:
            pytest.fail(f"Should propagate menu system errors: {e}")
    
    @patch('builtins.input', side_effect=['0'])  # Exit immediately
    @patch('task1.src.database_loader.get_all_records')
    def test_run_crud_operations_handles_exit_variants(self, mock_records, mock_input):
        """Test CRUD operations accepts various exit commands."""
        exit_commands = ['back', '0', 'exit', 'quit']
        
        for cmd in exit_commands:
            with patch('builtins.input', side_effect=[cmd]):
                # Should exit cleanly without errors
                try:
                    run_crud_operations("test.db")
                except Exception as e:
                    pytest.fail(f"Exit command '{cmd}' should work cleanly: {e}")


class TestIntegration:
    """Integration tests for main CLI components."""
    
    @patch('task1.src.menu_cli.run_menu_system')
    def test_data_analysis_pipeline_integration(self, mock_menu, capsys):
        """Test complete data analysis pipeline flow."""
        test_db = "task1/data/CLI_demo.db"
        
        # Run data analysis
        run_data_analysis(test_db)
        
        # Verify menu system called with correct path
        mock_menu.assert_called_once_with(test_db)
        
        # Check output formatting
        captured = capsys.readouterr()
        assert len(captured.out) > 0, "Should produce output"
        assert "=" in captured.out, "Should have formatted output"
    
    @patch('builtins.input', side_effect=['help', 'list', 'back'])
    @patch('task1.src.database_loader.get_all_records', return_value=[])
    def test_crud_operations_workflow(self, mock_records, mock_input, capsys):
        """Test typical CRUD operations workflow."""
        test_db = "test.db"
        
        run_crud_operations(test_db)
        
        captured = capsys.readouterr()
        
        # Should show help
        assert 'help' in captured.out.lower() or 'command' in captured.out.lower()
        
        # Should attempt to list records
        mock_records.assert_called()
        
        # Should exit cleanly
        assert 'Returning' in captured.out or 'menu' in captured.out


class TestTypeAnnotations:
    """Test that functions have proper type hints."""
    
    def test_functions_have_type_hints(self):
        """Verify key functions have type annotations."""
        import inspect
        
        # Check run_data_analysis has db_path parameter with str type
        sig = inspect.signature(run_data_analysis)
        assert 'db_path' in sig.parameters
        assert sig.parameters['db_path'].annotation == str
        
        # Check run_crud_operations has db_path parameter with str type
        sig = inspect.signature(run_crud_operations)
        assert 'db_path' in sig.parameters
        assert sig.parameters['db_path'].annotation == str


class TestDocstrings:
    """Test that functions have proper documentation."""
    
    def test_functions_have_docstrings(self):
        """Verify all main functions have docstrings."""
        functions = [
            print_welcome,
            print_main_menu,
            run_data_analysis,
            run_crud_operations,
            run_create_database
        ]
        
        for func in functions:
            assert func.__doc__ is not None, f"{func.__name__} should have docstring"
            assert len(func.__doc__.strip()) > 0, f"{func.__name__} docstring should not be empty"
    
    def test_docstrings_are_descriptive(self):
        """Test that docstrings contain meaningful descriptions."""
        # run_data_analysis should mention menu or analysis
        doc = run_data_analysis.__doc__.lower()
        assert 'menu' in doc or 'analysis' in doc or 'launch' in doc
        
        # run_crud_operations should mention CRUD or operations
        doc = run_crud_operations.__doc__.lower()
        assert 'crud' in doc or 'operation' in doc


# Run pytest with: pytest task1/test_main.py -v
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
