# Database Files Overview

Quick reference for database files in `task1/data/`.

---

## 📊 Active Databases

### `life_expectancy.db` (664 KB) - **PRODUCTION**

**Data:** 3,111 records | 183 countries | 2000-2016  
**Source:** `life_expectancy_cleaned.csv` (cleaned by pipeline)  
**Purpose:** Main database for queries, analysis, and visualization  

**⚠️ NEVER MODIFY** - Read-only production data

**Recreate:**
```bash
python task1/pipeline_clean_export.py  # Clean CSV
python -c "from task1.database_loader import create_database, load_data_to_db; \
           from task1.data_loader import load_csv; \
           create_database('task1/data/life_expectancy.db'); \
           load_data_to_db('task1/data/life_expectancy.db', \
                          load_csv('task1/data/life_expectancy_cleaned.csv'))"
```

---

### `CLI_demo.db` (28 KB) - **DEVELOPMENT**

**Data:** 12 records | 4 countries (China, India, USA, Brazil) | 2015-2017  
**Source:** `conftest.py` test sample data  
**Purpose:** Fast CLI testing and CRUD operations practice

**Why small data?**
- Quick operations (milliseconds)
- Matches pytest test data (easy verification)
- Safe to modify/delete

**Recreate:**
```bash
python task1/create_demo_db.py
```

**Usage:**
```bash
# CLI default database for testing
python task1/cli.py info
python task1/cli.py filter --country China

# CRUD operations (safe to modify)
python task1/cli.py --db CLI_demo.db create --country Japan --year 2020
```

---

### `crud_demo.db` (28 KB) - **AUTO-GENERATED**

**Data:** 5 records (temporary demo data)  
**Purpose:** Automated CRUD demonstration script  
**Lifecycle:** Auto-created and destroyed by `demo_crud.py`

**Not for manual use** - Automatically managed by demo script

```bash
python task1/demo_crud.py  # Creates, demos CRUD, shows results
```

---

## 🔒 Safety Rules

| Database | Modify? | Use Case |
|----------|---------|----------|
| `life_expectancy.db` | ❌ Never | Production queries/analysis |
| `CLI_demo.db` | ✅ Safe | Development/CRUD testing |
| `crud_demo.db` | 🤖 Auto | Demo script only |

**CRUD operations must use `CLI_demo.db` - Production database is read-only!**

---

## 📐 Database Schema

All databases share this structure:

```sql
CREATE TABLE life_expectancy (
    country TEXT NOT NULL,
    region TEXT,
    year INTEGER NOT NULL,
    life_expect REAL,
    bmi REAL,
    water_access REAL,
    sanitation_access REAL,
    PRIMARY KEY (country, year)
);
```

Indexes: `country`, `region`, `year`

---

## 🔄 Maintenance

**Recreate production database:**
```bash
python task1/pipeline_clean_export.py  # Step 1: Clean data
# Step 2: Create database (see command above)
```

**Recreate demo database:**
```bash
python task1/create_demo_db.py
```

**Run CRUD demonstration:**
```bash
python task1/demo_crud.py
```

---

## 🛠️ Troubleshooting

**Database locked:**
- Close all connections (files auto-close after operations)

**Missing CLI_demo.db:**
```bash
python task1/create_demo_db.py
```

**Corrupted database:**
- Delete and recreate using commands above

---

**Last Updated:** December 23, 2025  
**Project:** PAI Individual Assignment - Task 1
