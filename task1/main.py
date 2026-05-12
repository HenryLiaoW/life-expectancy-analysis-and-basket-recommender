#!/usr/bin/env python3
"""
Main Entry Point for Life Expectancy Data System
=================================================

Unified interface for:
1. Data Analysis (filtering, cleaning, visualization)
2. Database CRUD Operations (create, read, update, delete)

Author: Suhang Liao
Module: Programming for Artificial Intelligence WM9QF-15
"""

import sys
import os

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from task1.config import RAW_LIFE_EXPECTANCY_CSV, TEST_DATABASE, DEMO_DATABASE


def print_welcome():
    """Print welcome banner."""
    print("\n" + "="*60)
    print(" Life Expectancy Data Insights System")
    print("="*60)
    print(" WHO Public Health Data Analysis & Management")
    print("="*60)


def print_main_menu():
    """Print main menu options."""
    print("\n📋 Main Menu:")
    print("  1 - Data Analysis Pipeline")
    print("      (Filter, Clean, Analyze, Visualize)")
    print()
    print("  2 - Database CRUD Operations")
    print("      (Create, Read, Update, Delete records)")
    print()
    print("  3 - Create Database from CSV")
    print("      (Convert CSV file to SQLite database)")
    print()
    print("  0 - Exit")


def run_data_analysis(db_path: str):
    """Launch data analysis menu."""
    from task1.src.menu_cli import run_menu_system
    
    print("\n🔄 Launching Data Analysis Pipeline...")
    print("="*60)
    
    run_menu_system(db_path)


def run_crud_operations(db_path: str):
    """Launch CRUD operations CLI - Interactive mode."""
    from task1.src.database_loader import (
        create_record, get_records_by_country, 
        update_record, delete_record, get_all_records
    )
    
    print("\n🔄 Launching CRUD Operations Interface...")
    print("="*60)
    print("\n💡 Available commands:")
    print("  • create  - Add new record")
    print("  • read    - Query records by country")
    print("  • update  - Update existing record")
    print("  • delete  - Remove record")
    print("  • list    - Show all records")
    print("  • help    - Show this help")
    print("="*60)
    
    while True:
        print("\n" + "-"*60)
        cmd = input("📝 CRUD command (or 'back' to return): ").strip().lower()
        
        if cmd in ['back', '0', 'exit', 'quit']:
            print("\n↩️  Returning to main menu...")
            break
        
        elif cmd == 'create':
            print("\n" + "="*60)
            print("CREATE NEW RECORD")
            print("="*60)
            print("\n📋 Required fields (country, year, region, life_expect)")
            
            try:
                country = input("Country: ").strip()
                year = int(input("Year: ").strip())
                region = input("Region: ").strip()
                life_expect = float(input("Life Expectancy: ").strip())
                
                # Optional fields
                print("\n📝 Optional fields (press Enter to skip):")
                adult_mort = input("Adult Mortality: ").strip()
                infant_mort = input("Infant Deaths: ").strip()
                alcohol = input("Alcohol: ").strip()
                bmi = input("BMI: ").strip()
                
                # Build record
                record = {
                    'country': country,
                    'year': year,
                    'region': region,
                    'life_expect': life_expect
                }
                if adult_mort: record['adult_mortality'] = float(adult_mort)
                if infant_mort: record['infant_mort'] = float(infant_mort)
                if alcohol: record['alcohol'] = float(alcohol)
                if bmi: record['bmi'] = float(bmi)
                
                create_record(db_path, record)
                print(f"\n✅ Record created: {country} ({year})")
                
            except ValueError as e:
                print(f"\n❌ Invalid input: {e}")
            except Exception as e:
                print(f"\n❌ Error: {e}")
        
        elif cmd == 'read':
            country = input("Enter country name: ").strip()
            try:
                records = get_records_by_country(db_path, country)
                if records:
                    print(f"\n📊 Found {len(records)} records for {country}")
                    print("="*60)
                    
                    for r in records[:10]:  # Show first 10
                        print(f"\n🔍 Record: {r['country']} ({r['year']})")
                        print("-"*60)
                        
                        # Display all fields - 使用真实数据库字段
                        print("📍 Basic Info:")
                        print(f"  • Country Code: {r.get('country_code', 'N/A')}")
                        print(f"  • Region: {r.get('region', 'N/A')}")
                        print(f"  • Life Expectancy: {r.get('life_expect', 'N/A')}")
                        print(f"  • Life Expectancy at 60: {r.get('life_exp60', 'N/A')}")
                        
                        print("\n💊 Mortality Indicators:")
                        print(f"  • Adult Mortality: {r.get('adult_mortality', 'N/A')}")
                        print(f"  • Infant Mortality: {r.get('infant_mort', 'N/A')}")
                        print(f"  • Age 1-4 Mortality: {r.get('age1-4mort', 'N/A')}")
                        
                        print("\n🏥 Health & Lifestyle:")
                        print(f"  • Alcohol Consumption: {r.get('alcohol', 'N/A')}")
                        print(f"  • BMI: {r.get('bmi', 'N/A')}")
                        print(f"  • Age 5-19 Thinness: {r.get('age5-19thinness', 'N/A')}")
                        print(f"  • Age 5-19 Obesity: {r.get('age5-19obesity', 'N/A')}")
                        
                        print("\n💉 Immunization Coverage:")
                        print(f"  • Hepatitis: {r.get('hepatitis', 'N/A')}")
                        print(f"  • Measles: {r.get('measles', 'N/A')}")
                        print(f"  • Polio: {r.get('polio', 'N/A')}")
                        print(f"  • Diphtheria: {r.get('diphtheria', 'N/A')}")
                        
                        print("\n🌍 Infrastructure & Resources:")
                        print(f"  • Basic Water Access: {r.get('basic_water', 'N/A')}")
                        print(f"  • Doctors per 10k: {r.get('doctors', 'N/A')}")
                        print(f"  • Hospital Beds per 10k: {r.get('hospitals', 'N/A')}")
                        
                        print("\n💰 Economic Indicators:")
                        print(f"  • GNI per Capita: {r.get('gni_capita', 'N/A')}")
                        print(f"  • Gov Health Expenditure (% of GDP): {r.get('gghe-d', 'N/A')}")
                        print(f"  • Current Health Exp (% of GDP): {r.get('che_gdp', 'N/A')}")
                        
                        print("\n👶 UNESCO Indicators:")
                        print(f"  • Population: {r.get('une_pop', 'N/A')}")
                        print(f"  • Infant Deaths (UNE): {r.get('une_infant', 'N/A')}")
                        print(f"  • Life Expectancy (UNE): {r.get('une_life', 'N/A')}")
                        print(f"  • HIV Prevalence: {r.get('une_hiv', 'N/A')}")
                        print(f"  • GNI (UNE): {r.get('une_gni', 'N/A')}")
                        print(f"  • Poverty Rate: {r.get('une_poverty', 'N/A')}")
                        print(f"  • Education Spending: {r.get('une_edu_spend', 'N/A')}")
                        print(f"  • Literacy Rate: {r.get('une_literacy', 'N/A')}")
                        print(f"  • School Enrollment: {r.get('une_school', 'N/A')}")
                        
                        if len(records) > 1:
                            print("\n" + "="*60)
                    
                    if len(records) > 10:
                        print(f"\n... and {len(records) - 10} more records")
                else:
                    print(f"\n❌ No records found for {country}")
            except Exception as e:
                print(f"\n❌ Error: {e}")
        
        elif cmd == 'update':
            print("\n" + "="*60)
            print("UPDATE RECORD")
            print("="*60)
            
            try:
                country = input("Country: ").strip()
                year = int(input("Year: ").strip())
                
                print("\n📝 Enter new values (press Enter to skip):")
                updates = {}
                
                # Core metrics
                life_expect = input("Life Expectancy: ").strip()
                if life_expect: updates['life_expect'] = float(life_expect)
                
                adult_mort = input("Adult Mortality: ").strip()
                if adult_mort: updates['adult_mortality'] = float(adult_mort)
                
                infant_mort = input("Infant Mortality: ").strip()
                if infant_mort: updates['infant_mort'] = float(infant_mort)
                
                # Healthcare
                alcohol = input("Alcohol: ").strip()
                if alcohol: updates['alcohol'] = float(alcohol)
                
                bmi = input("BMI: ").strip()
                if bmi: updates['bmi'] = float(bmi)
                
                # Immunization
                polio = input("Polio (%): ").strip()
                if polio: updates['polio'] = float(polio)
                
                diphtheria = input("Diphtheria (%): ").strip()
                if diphtheria: updates['diphtheria'] = float(diphtheria)
                
                # Infrastructure
                basic_water = input("Basic Water (%): ").strip()
                if basic_water: updates['basic_water'] = float(basic_water)
                
                if updates:
                    update_record(db_path, country, year, updates)
                    print(f"\n✅ Record updated: {country} ({year})")
                    print(f"   Updated {len(updates)} field(s): {', '.join(updates.keys())}")
                else:
                    print("\n⚠️  No updates provided")
                    
            except ValueError as e:
                print(f"\n❌ Invalid input: {e}")
            except Exception as e:
                print(f"\n❌ Error: {e}")
        
        elif cmd == 'delete':
            print("\n" + "="*60)
            print("DELETE RECORD")
            print("="*60)
            
            try:
                country = input("Country: ").strip()
                year = int(input("Year: ").strip())
                
                confirm = input(f"\n⚠️  Delete {country} ({year})? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    delete_record(db_path, country, year)
                    print(f"\n✅ Record deleted: {country} ({year})")
                else:
                    print("\n❌ Deletion cancelled")
                    
            except Exception as e:
                print(f"\n❌ Error: {e}")
        
        elif cmd == 'list':
            try:
                records = get_all_records(db_path)
                print(f"\n📊 Total records: {len(records)}")
                print("-"*60)
                
                # Group by country
                countries = {}
                for r in records:
                    c = r['country']
                    if c not in countries:
                        countries[c] = []
                    countries[c].append(r['year'])
                
                for country in sorted(countries.keys())[:20]:  # Show first 20
                    years = sorted(countries[country])
                    print(f"  {country:20} {len(years)} records ({years[0]}-{years[-1]})")
                
                if len(countries) > 20:
                    print(f"\n  ... and {len(countries) - 20} more countries")
                    
            except Exception as e:
                print(f"\n❌ Error: {e}")
        
        elif cmd == 'help':
            print("\n📖 CRUD Operations Help:")
            print("-"*60)
            print("  create - Add a new record (interactive prompts)")
            print("  read   - Query records by country name")
            print("  update - Modify an existing record")
            print("  delete - Remove a record (with confirmation)")
            print("  list   - Display all records summary")
            print("  back   - Return to main menu")
            print("-"*60)
        
        else:
            print(f"\n❌ Unknown command: '{cmd}'")
            print("💡 Type 'help' for available commands")

def run_create_database():
    """Interactive database creation from CSV.
    
    Returns:
        str: Path to created database, or None if cancelled/failed
    """
    from task1.src.create_db import create_db_from_csv
    
    print("\n🔄 Database Creation from CSV")
    print("="*60)
    
    # Ask for CSV path
    print("\n📂 CSV File:")
    print(f"  1 - Full dataset ({RAW_LIFE_EXPECTANCY_CSV})")
    print("  2 - Custom CSV file")
    print("  3 - Demo data (12 records)")
    
    choice = input("\nSelect CSV source: ").strip()
    
    if choice == '1':
        csv_path = str(RAW_LIFE_EXPECTANCY_CSV)
        db_default = str(TEST_DATABASE)
        use_demo = False
    elif choice == '2':
        csv_path = input("Enter CSV file path: ").strip()
        if not os.path.exists(csv_path):
            print(f"\n❌ File not found: {csv_path}")
            return None
        db_default = csv_path.replace('.csv', '.db')
        use_demo = False
    elif choice == '3':
        csv_path = None
        db_default = str(DEMO_DATABASE)
        use_demo = True
    else:
        print("\n❌ Invalid choice")
        return None
    
    # Ask for database path
    print(f"\n💾 Output Database:")
    print(f"  Default: {db_default}")
    db_path = input(f"Enter path (or press Enter for default): ").strip()
    
    if not db_path:
        db_path = db_default
    
    # Confirm overwrite
    if os.path.exists(db_path):
        confirm = input(f"\n⚠️  Database exists. Overwrite? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("\n❌ Cancelled")
            return None
    
    # Create database
    try:
        print("\n🔨 Creating database...")
        print("="*60)
        
        created_db = create_db_from_csv(csv_path, db_path, use_demo)
        
        print("\n" + "="*60)
        print("✅ Database created successfully!")
        print("="*60)
        print(f"\n💾 Database path: {created_db}")
        
        return created_db
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main entry point."""
    import argparse
    
    # Get script directory to build absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_db = str(DEMO_DATABASE)
    
    parser = argparse.ArgumentParser(
        description="Life Expectancy Data Insights System - Main Entry Point"
    )
    parser.add_argument(
        "--db", 
        default=default_db,
        help=f"Path to SQLite database (default: {default_db})"
    )
    
    args = parser.parse_args()
    
    # Validate database exists
    if not os.path.exists(args.db):
        print(f"\n❌ Error: Database not found at {args.db}")
        print(f"💡 Available databases:")
        
        # Search in multiple locations
        search_paths = [
            os.path.join(script_dir, "data"),  # task1/data/
            os.path.join(project_root, "task1", "data")  # From project root
        ]
        
        for search_dir in search_paths:
            if os.path.exists(search_dir):
                for db in os.listdir(search_dir):
                    if db.endswith('.db'):
                        full_path = os.path.join(search_dir, db)
                        size = os.path.getsize(full_path)
                        print(f"   • {full_path} ({size:,} bytes)")
        sys.exit(1)
    
    print_welcome()
    
    # Main loop
    while True:
        print_main_menu()
        
        try:
            choice = input("\n👉 Select option: ").strip()
            
            if choice == '1':
                run_data_analysis(args.db)
                # Return to main menu after analysis
                print_welcome()
            
            elif choice == '2':
                run_crud_operations(args.db)
                # Return to main menu after CRUD
                print_welcome()
            
            elif choice == '3':
                new_db = run_create_database()
                if new_db:
                    # Ask if user wants to switch to new database
                    print("\n" + "="*60)
                    switch = input("\n🔄 Switch to new database and continue? (yes/no): ").strip().lower()
                    if switch == 'yes':
                        args.db = new_db
                        print(f"\n✅ Switched to: {new_db}")
                        print("\n💡 You can now use options 1 or 2 with this database")
                    else:
                        print(f"\n💡 Database created but not loaded.")
                        print(f"   Restart with: python task1/main.py --db {new_db}")
                else:
                    print("\n⚠️  Database creation cancelled or failed")
                
                input("\nPress Enter to return to main menu...")
                print_welcome()
            
            elif choice == '0':
                print("\n" + "="*60)
                print("👋 Thank you for using the system!")
                print("="*60)
                print()
                break
            
            else:
                print(f"\n❌ Invalid choice: {choice}")
                print("💡 Please enter 1, 2, or 0")
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            print("👋 Goodbye!")
            break
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
