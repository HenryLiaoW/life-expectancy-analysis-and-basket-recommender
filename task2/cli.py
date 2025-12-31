"""
Supermarket Recommendation System - Command Line Interface

This module provides an interactive CLI for exploring customer purchasing patterns
and generating product recommendations based on co-occurrence analysis.

Usage:
    python -m task2.cli
    or
    python task2/cli.py
"""

from pathlib import Path
from task2.src.recommendation_engine import RecommendationEngine


class SupermarketCLI:
    """
    Interactive command-line interface for supermarket recommendation system.
    
    Implements user-friendly menu-driven interaction with comprehensive
    error handling and formatted output display.
    """
    
    def __init__(self):
        """Initialize CLI with recommendation engine"""
        self.engine = RecommendationEngine()
        self.data_loaded = False
        self.dataset_path = Path(__file__).parent / "data" / "Supermarket_dataset_PAI.csv"
        
    def display_header(self):
        """Display application header with styling"""
        print("\n" + "=" * 70)
        print("  SUPERMARKET RECOMMENDATION SYSTEM")
        print("  Market Basket Analysis & Product Co-occurrence Engine")
        print("=" * 70)
        
    def display_menu(self):
        """Display main menu options"""
        print("\n--- MAIN MENU ---")
        print("1. Load Dataset")
        print("2. Single Item Recommendation (Requirement 1)")
        print("3. Most Frequent Product Pairs (Requirement 2)")
        print("4. Co-purchase Frequency Check (Requirement 3)")
        print("5. Basket-based Recommendation (Extension)")
        print("6. Dynamic Update Simulation (Extension)")
        print("7. Visualize Graph Structure (Visualization)")
        print("8. System Statistics")
        print("0. Exit")
        print("-" * 50)
        
    def load_data(self):
        """
        Load dataset with error handling and user feedback.
        
        Returns:
            bool: True if successfully loaded, False otherwise
        """
        if self.data_loaded:
            print("\n⚠️  Dataset already loaded!")
            choice = input("Reload? (y/n): ").strip().lower()
            if choice != 'y':
                return True
                
        try:
            print(f"\n📂 Loading dataset from: {self.dataset_path}")
            print("⏳ Processing transactions and building graph...")
            
            self.engine.load_data(str(self.dataset_path))
            self.data_loaded = True
            
            # Display statistics
            all_items = self.engine.graph.get_all_items()
            print(f"\n✅ Dataset loaded successfully!")
            print(f"   Total unique items: {len(all_items)}")
            print(f"   Total edges (co-occurrences): {self.engine.graph.num_edges}")
            
            return True
            
        except FileNotFoundError:
            print(f"\n❌ Error: Dataset not found at {self.dataset_path}")
            print("   Please ensure the data file exists in task2/data/")
            return False
        except Exception as e:
            print(f"\n❌ Error loading dataset: {str(e)}")
            return False
            
    def recommend_for_item(self):
        """
        Requirement 1: Single item recommendation.
        "What else do customers who bought bread buy?"
        """
        if not self._check_data_loaded():
            return
            
        print("\n--- SINGLE ITEM RECOMMENDATION ---")
        item = input("Enter product name: ").strip()
        
        if not item:
            print("❌ Item name cannot be empty")
            return
            
        try:
            k = int(input("Number of recommendations (default 5): ").strip() or "5")
            if k <= 0:
                print("❌ Number must be positive")
                return
        except ValueError:
            print("❌ Invalid number")
            return
            
        # Check if item exists
        if not self.engine.graph.has_item(item):
            print(f"\n⚠️  Item '{item}' not found in dataset")
            self._suggest_similar_items(item)
            return
            
        recommendations = self.engine.recommend_for_item(item, top_k=k)
        
        if not recommendations:
            print(f"\n⚠️  No co-purchase data available for '{item}'")
            return
        
        print(f"\n✓ Found only {len(recommendations)} items related to '{item}'")
        print(f"\n📊 Top {len(recommendations)} items frequently bought with '{item}':")
        print("-" * 70)
        print(f"{'Rank':<6} {'Product Name':<40} {'Co-purchase Count':>20}")
        print("-" * 70)
        
        for rank, (product, count) in enumerate(recommendations, 1):
            print(f"{rank:<6} {product:<40} {count:>20}")
            
        print("-" * 70)
        
    def get_most_frequent_pairs(self):
        """
        Requirement 2: Most frequent co-purchase pairs.
        "Which product combinations are most frequently bought together?"
        """
        if not self._check_data_loaded():
            return
            
        print("\n--- MOST FREQUENT PRODUCT PAIRS ---")
        
        try:
            k = int(input("Number of pairs to display (default 10): ").strip() or "10")
            if k <= 0:
                print("❌ Number must be positive")
                return
        except ValueError:
            print("❌ Invalid number")
            return
            
        pairs = self.engine.get_most_frequent_pairs(top_k=k)
        
        if not pairs:
            print("\n⚠️  No co-purchase pairs found")
            return
            
        print(f"\n📊 Top {len(pairs)} most frequently co-purchased product pairs:")
        print("-" * 80)
        print(f"{'Rank':<6} {'Product 1':<25} {'Product 2':<25} {'Frequency':>20}")
        print("-" * 80)
        
        for rank, ((item1, item2), count) in enumerate(pairs, 1):
            print(f"{rank:<6} {item1:<25} {item2:<25} {count:>20}")
            
        print("-" * 80)
        
    def check_co_purchase(self):
        """
        Requirement 3: Co-purchase frequency check.
        "Are two items frequently bought together?"
        """
        if not self._check_data_loaded():
            return
            
        print("\n--- CO-PURCHASE FREQUENCY CHECK ---")
        item1 = input("Enter first product name: ").strip()
        item2 = input("Enter second product name: ").strip()
        
        if not item1 or not item2:
            print("❌ Product names cannot be empty")
            return
            
        try:
            threshold = int(input("Frequency threshold (default 50): ").strip() or "50")
            if threshold < 0:
                print("❌ Threshold must be non-negative")
                return
        except ValueError:
            print("❌ Invalid threshold")
            return
            
        # Check if items exist
        if not self.engine.graph.has_item(item1):
            print(f"\n⚠️  Item '{item1}' not found in dataset")
            return
        if not self.engine.graph.has_item(item2):
            print(f"\n⚠️  Item '{item2}' not found in dataset")
            return
            
        # Get actual count
        actual_count = self.engine.get_pair_count(item1, item2)
        is_frequent = self.engine.check_co_purchase(item1, item2, threshold)
        
        print("\n" + "=" * 70)
        print(f"Product Pair: '{item1}' ↔ '{item2}'")
        print("-" * 70)
        print(f"Co-purchase frequency: {actual_count}")
        print(f"Threshold: {threshold}")
        print(f"Frequently purchased together: {'✅ YES' if is_frequent else '❌ NO'}")
        print("=" * 70)
        
    def recommend_for_basket(self):
        """
        Extension: Basket-based recommendation.
        "Recommend items based on current shopping basket"
        """
        if not self._check_data_loaded():
            return
            
        print("\n--- BASKET-BASED RECOMMENDATION ---")
        print("Enter items in current basket (comma-separated):")
        basket_input = input("Items: ").strip()
        
        if not basket_input:
            print("❌ Basket cannot be empty")
            return
            
        basket = [item.strip() for item in basket_input.split(',')]
        
        # Validate items
        invalid_items = [item for item in basket if not self.engine.graph.has_item(item)]
        if invalid_items:
            print(f"\n⚠️  Items not found: {', '.join(invalid_items)}")
            return
            
        try:
            k = int(input("Number of recommendations (default 5): ").strip() or "5")
            if k <= 0:
                print("❌ Number must be positive")
                return
        except ValueError:
            print("❌ Invalid number")
            return
            
        recommendations = self.engine.recommend_for_basket(basket, top_k=k)
        
        if not recommendations:
            print("\n⚠️  No recommendations available for this basket")
            return
            
        print(f"\n🛒 Current basket: {', '.join(basket)}")
        print(f"\n📊 Top {len(recommendations)} recommended items to add:")
        print("-" * 70)
        print(f"{'Rank':<6} {'Product Name':<40} {'Aggregated Score':>20}")
        print("-" * 70)
        
        for rank, (product, score) in enumerate(recommendations, 1):
            print(f"{rank:<6} {product:<40} {score:>20}")
            
        print("-" * 70)
        
    def simulate_dynamic_update(self):
        """
        Extension: Dynamic update simulation.
        "Simulate real-time transaction updates"
        """
        if not self._check_data_loaded():
            return
            
        print("\n--- DYNAMIC UPDATE SIMULATION ---")
        print("Simulate a new transaction to update the recommendation system")
        print("Enter items purchased (comma-separated):")
        transaction_input = input("Items: ").strip()
        
        if not transaction_input:
            print("❌ Transaction cannot be empty")
            return
            
        items = [item.strip() for item in transaction_input.split(',')]
        
        # Show before state for first pair
        if len(items) >= 2:
            before_count = self.engine.get_pair_count(items[0], items[1])
            print(f"\n📊 Before update: '{items[0]}' ↔ '{items[1]}' count = {before_count}")
        
        # Update
        self.engine.update_with_transaction(items)
        print("\n✅ Transaction processed successfully!")
        
        # Show after state
        if len(items) >= 2:
            after_count = self.engine.get_pair_count(items[0], items[1])
            print(f"📊 After update: '{items[0]}' ↔ '{items[1]}' count = {after_count}")
            print(f"   Change: +{after_count - before_count}")
            
        # Show recommendation impact
        if len(items) >= 1:
            print(f"\n📈 Updated recommendations for '{items[0]}':")
            recommendations = self.engine.recommend_for_item(items[0], top_k=5)
            for rank, (product, count) in enumerate(recommendations, 1):
                print(f"   {rank}. {product} (count: {count})")
                
    def show_statistics(self):
        """Display system statistics and information"""
        if not self._check_data_loaded():
            return
            
        print("\n--- SYSTEM STATISTICS ---")
        all_items = self.engine.graph.get_all_items()
        
        print(f"Total unique items: {len(all_items)}")
        print(f"Total edges (co-occurrences): {self.engine.graph.num_edges}")
        
        # Find top 5 most connected items
        print("\n📊 Top 5 most connected items:")
        item_connections = []
        for item in all_items:
            neighbors = self.engine.graph.get_neighbors(item)
            item_connections.append((item, len(neighbors)))
        
        item_connections.sort(key=lambda x: -x[1])
        
        for rank, (item, conn_count) in enumerate(item_connections[:5], 1):
            print(f"   {rank}. {item:<30} ({conn_count} connections)")
    
    def visualize_graph(self):
        """
        Visualization Extension: Display graph structure
        """
        if not self._check_data_loaded():
            return
        
        print("\n--- GRAPH VISUALIZATION ---")
        print("1. ASCII Subgraph (item neighborhood)")
        print("2. Export to DOT format (Graphviz)")
        print("0. Back to main menu")
        
        choice = input("\nSelect visualization type: ").strip()
        
        if choice == '0':
            return
        elif choice == '1':
            # ASCII subgraph visualization
            item = input("\nEnter item name to visualize: ").strip()
            if not item:
                print("❌ Item name cannot be empty")
                return
            
            if not self.engine.graph.has_item(item):
                print(f"\n⚠️  Item '{item}' not found")
                self._suggest_similar_items(item)
                return
            
            try:
                max_neighbors = int(input("Max neighbors to show (default 10): ").strip() or "10")
                if max_neighbors <= 0:
                    print("❌ Number must be positive")
                    return
            except ValueError:
                print("❌ Invalid number")
                return
            
            visualization = self.engine.graph.visualize_subgraph(item, max_neighbors)
            print(visualization)
            
        elif choice == '2':
            # Export to DOT format
            output_file = input("\nOutput filename (default: graph.dot): ").strip() or "graph.dot"
            
            try:
                max_edges = int(input("Max edges to export (0=all, default 100): ").strip() or "100")
                if max_edges < 0:
                    print("❌ Number cannot be negative")
                    return
            except ValueError:
                print("❌ Invalid number")
                return
            
            output_path = Path(__file__).parent / output_file
            result = self.engine.graph.export_to_dot(str(output_path), max_edges)
            print(f"\n{result}")
            
            if result.startswith("✓"):
                print(f"\n💡 To visualize:")
                print(f"   1. Install Graphviz: https://graphviz.org/download/")
                print(f"   2. Run: dot -Tpng {output_file} -o graph.png")
                print(f"   3. Or use online viewer: http://www.webgraphviz.com/")
        else:
            print("❌ Invalid choice")
            
    def _check_data_loaded(self):
        """
        Check if dataset is loaded, prompt user if not.
        
        Returns:
            bool: True if data is loaded, False otherwise
        """
        if not self.data_loaded:
            print("\n⚠️  Please load dataset first (Option 1)")
            return False
        return True
        
    def _suggest_similar_items(self, item):
        """
        Suggest similar item names (simple case-insensitive matching).
        
        Args:
            item: User input item name
        """
        all_items = self.engine.graph.get_all_items()
        item_lower = item.lower()
        
        # Find items containing the search term
        suggestions = [i for i in all_items if item_lower in i.lower()][:5]
        
        if suggestions:
            print("\n💡 Did you mean one of these?")
            for suggestion in suggestions:
                print(f"   - {suggestion}")
                
    def run(self):
        """Main application loop"""
        self.display_header()
        
        while True:
            self.display_menu()
            
            try:
                choice = input("\nEnter your choice: ").strip()
                
                if choice == '0':
                    print("\n👋 Thank you for using Supermarket Recommendation System!")
                    print("   Exiting...\n")
                    break
                    
                elif choice == '1':
                    self.load_data()
                    
                elif choice == '2':
                    self.recommend_for_item()
                    
                elif choice == '3':
                    self.get_most_frequent_pairs()
                    
                elif choice == '4':
                    self.check_co_purchase()
                    
                elif choice == '5':
                    self.recommend_for_basket()
                    
                elif choice == '6':
                    self.simulate_dynamic_update()
                    
                elif choice == '7':
                    self.visualize_graph()
                    
                elif choice == '8':
                    self.show_statistics()
                    
                else:
                    print("\n❌ Invalid choice. Please enter 0-8.")
                    
                # Pause for user to read output
                if choice != '0':
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n⚠️  Operation cancelled by user")
                print("👋 Exiting...\n")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {str(e)}")
                print("   Please try again or contact support.")


def main():
    """Entry point for CLI application"""
    cli = SupermarketCLI()
    cli.run()


if __name__ == "__main__":
    main()
