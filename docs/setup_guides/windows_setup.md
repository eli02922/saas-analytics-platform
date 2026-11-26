# Windows 11 Setup Guide - SaaS Analytics Platform

## Prerequisites

Before starting, ensure you have:

1. **Windows 11** (or Windows 10/Server 2019+)
2. **Git** installed (https://git-scm.com/download/win)
3. **Python 3.11** installed (https://www.python.org/downloads/)
4. **A Snowflake account** (https://signup.snowflake.com - free trial available)
5. **Power BI Desktop** (optional, https://powerbi.microsoft.com/en-us/desktop/)

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/saas-analytics-platform.git
cd saas-analytics-platform
```

## Step 2: Create Virtual Environment

```bash
# Create Python virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Your prompt should now show (venv) prefix
```

## Step 3: Install Python Dependencies

```bash
# Upgrade pip, setuptools, and wheel
python -m pip install --upgrade pip setuptools wheel

# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list
```

## Step 4: Configure Environment Variables

```bash
# Copy the example .env file
copy .env.example .env

# Edit .env with your Snowflake credentials
# Open in your preferred editor (VS Code, Notepad++, etc.)
# Fields to fill in:
#   - SNOWFLAKE_ACCOUNT: your_account_id (from Snowflake account URL)
#   - SNOWFLAKE_USER: your_username
#   - SNOWFLAKE_PASSWORD: your_password
#   - SNOWFLAKE_WAREHOUSE: COMPUTE_S (or your warehouse name)
```

## Step 5: Verify Snowflake Connection

```bash
# Create a simple test script
python -c "
import os
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

try:
    conn = snowflake.connector.connect(
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE')
    )
    cur = conn.cursor()
    cur.execute('SELECT 1')
    print('✓ Snowflake connection successful!')
    cur.close()
    conn.close()
except Exception as e:
    print(f'✗ Connection failed: {e}')
"
```

## Step 6: Set Up Snowflake Database

1. Connect to Snowflake using their web UI (console.snowflake.com)
2. Run the setup scripts:

```bash
cd sql\snowflake\setup

# Execute scripts in order using Snowflake web UI's SQL worksheet:
# 1. 01_create_database.sql
# 2. 02_create_schemas.sql
# 3. 03_create_warehouses.sql
# 4. 04_create_roles.sql
# 5. 05_grant_permissions.sql
```

Or use Snowflake CLI (if installed):

```bash
snowsql -a your_account_id -u your_username -f 01_create_database.sql
```

## Step 7: Configure dbt

```bash
# Navigate to dbt project directory
cd dbt_project

# Create dbt profiles.yml in %USERPROFILE%\.dbt\
# File path: C:\Users\YourUsername\.dbt\profiles.yml

# Content:
saas_analytics:
  outputs:
    dev:
      type: snowflake
      account: your_account_id
      user: your_username
      password: your_password
      database: SAAS_ANALYTICS
      schema: SILVER
      warehouse: COMPUTE_S
      threads: 4
      client_session_keep_alive: false
  target: dev

# Test dbt connection
dbt debug

# Should show "All checks passed!"
```

## Step 8: Generate Synthetic Data

```bash
# From repository root
cd ..

# Generate synthetic data
python src\ingestion\generate_synthetic_data.py --config config\dev\config.yaml --size=small

# This creates sample data in memory and CSV files in dbt_project\data\
```

## Step 9: Run Python Ingestion

```bash
# Run data ingestion to Snowflake
python src\ingestion\run_ingestion.py --date 2024-01-01

# Monitor progress - should load:
# - Customers to raw_customers
# - Subscriptions to raw_subscriptions
# - Invoices to raw_invoices
# - Payments to raw_payments
# - Usage events to raw_product_usage
```

## Step 10: Run dbt Transformations

```bash
cd dbt_project

# Install dbt dependencies
dbt deps

# Run models in development schema
dbt run

# Run data quality tests
dbt test

# Generate documentation
dbt docs generate

# View documentation locally
dbt docs serve  # Open http://localhost:8000 in browser
```

## Step 11: Validate Transformation

```bash
# From dbt_project directory, run validation SQL
# In Snowflake web UI, run this query:

SELECT 
    'customers' as table_name, COUNT(*) as row_count FROM SAAS_ANALYTICS.GOLD.DIM_CUSTOMERS
UNION ALL
SELECT 'subscriptions', COUNT(*) FROM SAAS_ANALYTICS.GOLD.FCT_SUBSCRIPTIONS
UNION ALL
SELECT 'revenue', COUNT(*) FROM SAAS_ANALYTICS.GOLD.FCT_REVENUE
UNION ALL
SELECT 'payments', COUNT(*) FROM SAAS_ANALYTICS.GOLD.FCT_PAYMENTS
UNION ALL
SELECT 'activities', COUNT(*) FROM SAAS_ANALYTICS.GOLD.FCT_CUSTOMER_ACTIVITY;
```

## Step 12: Set Up Power BI (Optional)

1. Download and install **Power BI Desktop** (Windows only)
2. Open Power BI Desktop
3. Get Data → Snowflake Database
4. Enter your Snowflake connection details
5. Load tables from SAAS_ANALYTICS.GOLD schema
6. Create visualizations using provided DAX measures

## Troubleshooting

### Virtual Environment Issues

```bash
# If venv activation fails, try:
python -m venv venv
venv\Scripts\activate.bat  # Instead of .ps1

# Or use PowerShell with script execution policy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

### Snowflake Connection Issues

```bash
# Test Snowflake connectivity
python -c "import snowflake.connector; print('OK')"

# Check environment variables
echo %SNOWFLAKE_ACCOUNT%
echo %SNOWFLAKE_USER%
```

### dbt Issues

```bash
# Debug dbt
dbt debug --profile saas_analytics

# Check dbt version compatibility
dbt --version

# Clear dbt cache if models don't update
rmdir /s target\
rmdir /s dbt_packages\
dbt deps
```

### Python Package Installation Issues

```bash
# If pip install fails:
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir

# For specific packages:
pip install snowflake-connector-python --no-binary :all:
```

## Running Tests

```bash
# From repository root
pytest tests\ -v

# Run specific test file
pytest tests\unit\test_extractors.py -v

# Run with coverage
pytest tests\ --cov=src --cov-report=html
```

## Development Workflow

1. **Activate virtual environment:**
   ```bash
   venv\Scripts\activate
   ```

2. **Create feature branch:**
   ```bash
   git checkout -b feature/your-feature
   ```

3. **Make changes** to Python code, dbt models, or SQL

4. **Test locally:**
   ```bash
   pytest tests\ -v
   dbt run --select state:modified
   dbt test --select state:modified
   ```

5. **Commit changes:**
   ```bash
   git add .
   git commit -m "feat: add your feature"
   ```

6. **Push to GitHub:**
   ```bash
   git push origin feature/your-feature
   ```

## Next Steps

1. ✅ Windows local environment set up
2. → Run [Docker Setup Guide](./docker_setup.md) for Airflow (optional)
3. → Review [Data Dictionary](../data_dictionary/data_model.md)
4. → Set up Power BI dashboards
5. → Configure Airflow for orchestration

## Resources

- **Snowflake Documentation:** https://docs.snowflake.com/
- **dbt Documentation:** https://docs.getdbt.com/
- **Python Official:** https://www.python.org/
- **Git Documentation:** https://git-scm.com/doc
- **Power BI Documentation:** https://learn.microsoft.com/en-us/power-bi/

## Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Review error logs in `logs/` directory
3. Create an issue on GitHub with:
   - Your OS version
   - Python version (`python --version`)
   - Error message
   - Steps to reproduce

---

**Last Updated:** November 2024  
**Status:** Verified on Windows 11
