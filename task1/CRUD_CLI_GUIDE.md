# CRUD Operations CLI Guide

Interactive command-line interface for Create, Read, Update, Delete operations.

---

## 🎯 Design Philosophy

**Interactive Mode** - User-friendly prompts guide you through each field
- ✅ No need to remember 30+ field names
- ✅ Required fields enforced, optional fields skippable
- ✅ Confirmation before destructive operations
- ✅ Clear feedback and error messages

---

## 📝 CREATE - Add New Record

```bash
python task1/cli.py create
```

**Interactive Flow:**
```
✨ Create New Record (Interactive Mode)
======================================================================

Enter required fields (press Enter for optional fields):

Country (required): Japan
Year (required): 2020

Optional fields (press Enter to skip):

Region (e.g., Asia, Europe): Asia
Life Expectancy (years): 84.5
BMI (average): 23.2
Basic Water Access (%): 99.5
Health Expenditure (% GDP): 10.9
Alcohol Consumption (liters): 7.5
Polio Vaccination Coverage (%): 99
Diphtheria Vaccination Coverage (%): 99

----------------------------------------------------------------------
Record to be created:
  country: Japan
  year: 2020
  region: Asia
  life_expect: 84.5
  bmi: 23.2
  basic_water: 99.5
  gghe-d: 10.9
  alcohol: 7.5
  polio: 99.0
  diphtheria: 99.0
----------------------------------------------------------------------

Create this record? (yes/no): yes

✅ Record created successfully: Japan (2020)
```

---

## ✏️ UPDATE - Modify Existing Record

```bash
python task1/cli.py update
```

**Interactive Flow:**
```
✏️  Update Existing Record (Interactive Mode)
======================================================================

First, identify the record to update:

Country (required): China
Year (required): 2015

----------------------------------------------------------------------
Current record:
  Country: China
  Year: 2015
  Life Expectancy: 76.1
  BMI: 23.8
  Water Access: 95.5
----------------------------------------------------------------------

Enter new values (press Enter to keep current value):

Life Expectancy (years) [current: 76.1]: 76.5
BMI (average) [current: 23.8]: 24.0
Basic Water Access (%) [current: 95.5]: 
Health Expenditure (% GDP) [current: 3.2]: 3.5
Alcohol Consumption (liters) [current: 7.2]: 

----------------------------------------------------------------------
Fields to be updated:
  life_expect: 76.1 → 76.5
  bmi: 23.8 → 24.0
  gghe-d: 3.2 → 3.5
----------------------------------------------------------------------

Update this record? (yes/no): yes

✅ Record updated successfully: China (2015)
```

---

## 🗑️ DELETE - Remove Record

```bash
python task1/cli.py delete
```

**Interactive Flow:**
```
🗑️  Delete Record (Interactive Mode)
======================================================================

⚠️  WARNING: This operation cannot be undone!

Country (required): TestCountry
Year (required): 2020

----------------------------------------------------------------------
Record to be DELETED:
  Country: TestCountry
  Year: 2020
  Life Expectancy: 75.0
  BMI: 25.5
----------------------------------------------------------------------

⚠️  Delete this record? (yes/no): yes
⚠️  Are you absolutely sure? (type 'DELETE' to confirm): DELETE

✅ Record deleted successfully: TestCountry (2020)
```

---

## 🔒 Safety Features

### Production Database Protection

**Default database is demo.db** - Safe for testing
```bash
python task1/cli.py create  # Uses demo.db (12 records)
```

**Specify database explicitly** for other operations
```bash
python task1/cli.py --db task1/data/CLI_demo.db create
```

**Production database protection** (future enhancement)
```bash
python task1/cli.py --db task1/data/life_expectancy.db create
# Error: Cannot modify production database!
# Use --db CLI_demo.db for CRUD testing
```

### Validation

✅ **CREATE**: Prevents duplicate country-year combinations  
✅ **UPDATE**: Checks record exists before updating  
✅ **DELETE**: Double confirmation required  
✅ **All**: Input validation for numeric fields  

### Error Handling

```bash
# Example: Duplicate record
Country (required): China
Year (required): 2015
# ... fill fields ...
❌ Error: Record for China in year 2015 already exists.
Use update_record() to modify existing records.

# Example: Non-existent record
Country (required): Atlantis
Year (required): 2020
❌ No record found for Atlantis in year 2020
```

---

## 📊 READ Operations (Query)

Use existing CLI commands for reading data:

```bash
# Show all data
python task1/cli.py info

# Filter by country
python task1/cli.py filter --country Japan

# Filter with statistics
python task1/cli.py filter --country China --stats

# Compare multiple countries
python task1/cli.py compare China Japan USA
```

---

## 💡 Usage Tips

### Quick Testing Workflow

```bash
# 1. Create test record
python task1/cli.py create
# Country: TestCountry
# Year: 2020
# Life Expectancy: 75.0

# 2. Verify creation
python task1/cli.py filter --country TestCountry

# 3. Update values
python task1/cli.py update
# Country: TestCountry
# Year: 2020
# Life Expectancy: 76.0

# 4. Delete test record
python task1/cli.py delete
# Country: TestCountry
# Year: 2020
```

### Skip Optional Fields

Press **Enter** to skip any optional field:
```
BMI (average): [just press Enter]
Basic Water Access (%): [just press Enter]
```

### Cancel Operations

Type **no** or **n** at confirmation prompts to cancel:
```
Create this record? (yes/no): no
❌ Operation cancelled.
```

---

## 🎓 Educational Value (Distinction Criteria)

### User Experience Design
- **Progressive disclosure**: Required → Optional → Confirmation
- **Clear feedback**: Visual separators, status messages
- **Error prevention**: Validation, double confirmation for delete

### Software Engineering Principles
- **Separation of concerns**: CLI layer → Business logic layer
- **DRY**: Reusable input validation helpers
- **Defensive programming**: Comprehensive error handling

### Accessibility
- **No memorization required**: Fields prompted one by one
- **Visual hierarchy**: Boxes, separators, emojis for clarity
- **Reversible actions**: Confirmation before commits

---

## 🔍 Technical Implementation

```python
# Located in: task1/cli.py

class LifeExpectancyCLI:
    def cmd_create(self, args):
        # Interactive prompts for all fields
        # Validation + confirmation
        # Call database_loader.create_record()
    
    def cmd_update(self, args):
        # Identify record (country + year)
        # Show current values
        # Prompt for changes
        # Call database_loader.update_record()
    
    def cmd_delete(self, args):
        # Identify record
        # Show record to be deleted
        # Double confirmation
        # Call database_loader.delete_record()
```

**Backend Functions:**
- `task1/database_loader.py`: `create_record()`, `update_record()`, `delete_record()`
- Parameterized SQL queries (injection-safe)
- Transaction support with rollback
- Comprehensive validation

---

**Last Updated:** December 24, 2025  
**Project:** PAI Individual Assignment - Task 1
