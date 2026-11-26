# SaaS Analytics Engineering Platform

A production-grade, end-to-end analytics engineering platform that demonstrates enterprise data warehousing, transformation, and business intelligence practices using modern data stack technologies.

**[📋 Architecture Documentation](./ARCHITECTURE.md)** | **[🗂️ Project Structure](#project-structure)** | **[🚀 Quick Start](#quick-start)** | **[📊 Data Model](#data-model)** | **[✅ Testing](#testing-strategy)**

---

## 📌 Project Overview

This platform consolidates operational data from a SaaS business into a scalable analytics warehouse and transforms it into actionable business intelligence.

### Business Context

The platform models a SaaS company managing:
- **Customers** (~10,000 entities)
- **Subscriptions** (~15,000 entities)  
- **Invoices & Billing** (~50,000 records)
- **Payments** (~100,000 transactions)
- **Product Usage** (~250,000+ events)

### Key Analytics Delivered

- **ARR (Annual Recurring Revenue)** - Total annual revenue from active subscriptions
- **MRR (Monthly Recurring Revenue)** - Monthly recurring revenue snapshot
- **NRR (Net Revenue Retention)** - Revenue retention including expansion and churn
- **Customer Churn Rate** - Percentage of customers lost per period
- **Revenue Churn Rate** - Revenue lost from cancellations and downgrades
- **Customer Lifetime Value** - Expected total revenue per customer
- **Customer Growth** - Net new customer trends
- **Subscription Analytics** - Renewal, upgrade, and cancellation trends

---

## 🏗️ Architecture

### Medallion Architecture (Bronze → Silver → Gold)

```
SOURCE SYSTEMS (APIs, DBs)
        ↓
    PYTHON INGESTION
        ↓
  SNOWFLAKE BRONZE (Raw, immutable)
        ↓
  DBT SILVER (Cleaned, deduplicated)
        ↓
  DBT GOLD (Facts, dimensions, metrics)
        ↓
   POWER BI DASHBOARDS
```

### Data Layers

| Layer | Purpose | Characteristics |
|-------|---------|-----------------|
| **BRONZE** | Raw data storage | Immutable, timestamped, source-tracked |
| **SILVER** | Cleansed data | Deduplicated, validated, standardized |
| **GOLD** | Analytics-ready | Star schema, fact/dimension tables |
| **ANALYTICS** | Business metrics | Pre-calculated KPIs, marts, snapshots |

For detailed architecture diagrams and flow, see **[ARCHITECTURE.md](./ARCHITECTURE.md)**.

---

## 🗂️ Project Structure

```
saas-analytics-platform/
│
├── ARCHITECTURE.md                 # Detailed system and data architecture
├── README.md                        # This file
├── requirements.txt                # Python dependencies
│
├── config/                         # Configuration files
│   ├── dev/                        # Development configs
│   │   ├── dbt_profiles.yml
│   │   └── config.yaml
│   └── prod/                       # Production configs
│       ├── dbt_profiles.yml
│       └── config.yaml
│
├── docs/                           # Documentation
│   ├── architecture/               # Architecture diagrams
│   ├── data_dictionary/            # Data model documentation
│   │   └── data_model.md
│   ├── setup_guides/               # Installation guides
│   │   ├── windows_setup.md
│   │   ├── docker_setup.md
│   │   ├── snowflake_setup.md
│   │   ├── dbt_setup.md
│   │   ├── airflow_setup.md
│   │   └── powerbi_setup.md
│   └── business_metrics/           # Metric definitions
│       └── saas_metrics.md
│
├── dbt_project/                    # dbt transformation project
│   ├── dbt_project.yml             # dbt project configuration
│   ├── packages.yml                # dbt package dependencies
│   │
│   ├── models/
│   │   ├── staging/
│   │   │   ├── _sources.yml        # Source definitions
│   │   │   ├── stg_customers.sql
│   │   │   ├── stg_subscriptions.sql
│   │   │   ├── stg_invoices.sql
│   │   │   ├── stg_payments.sql
│   │   │   └── stg_product_usage.sql
│   │   │
│   │   ├── intermediate/
│   │   │   ├── int_customer_subscriptions.sql
│   │   │   ├── int_subscription_revenue.sql
│   │   │   ├── int_monthly_revenue.sql
│   │   │   └── int_customer_activity.sql
│   │   │
│   │   └── marts/
│   │       ├── dimensions/
│   │       │   ├── dim_customers.sql     # SCD Type 2
│   │       │   ├── dim_products.sql
│   │       │   ├── dim_subscriptions.sql
│   │       │   └── dim_date.sql
│   │       │
│   │       ├── facts/
│   │       │   ├── fct_subscriptions.sql
│   │       │   ├── fct_revenue.sql
│   │       │   ├── fct_payments.sql
│   │       │   └── fct_customer_activity.sql
│   │       │
│   │       └── metrics/
│   │           ├── mart_mrr.sql
│   │           ├── mart_arr.sql
│   │           ├── mart_customer_churn.sql
│   │           ├── mart_revenue_retention.sql
│   │           └── mart_customer_lifetime_value.sql
│   │
│   ├── snapshots/
│   │   └── customer_history.sql    # SCD Type 2 snapshot
│   │
│   ├── macros/                     # Jinja macros
│   │   ├── generate_alias_name.sql
│   │   └── business_logic/
│   │       ├── calc_mrr.sql
│   │       ├── calc_arr.sql
│   │       └── calc_churn.sql
│   │
│   ├── tests/
│   │   ├── generic/
│   │   │   └── test_no_negative_amounts.sql
│   │   │
│   │   └── data/
│   │       ├── test_mrr_calculation.sql
│   │       └── test_customer_uniqueness.sql
│   │
│   └── data/
│       └── sample_test_data.csv
│
├── src/                            # Python source code
│   │
│   ├── ingestion/                  # Data ingestion framework
│   │   ├── __init__.py
│   │   ├── config.py               # Ingestion configuration
│   │   │
│   │   ├── extractors/             # API/database extractors
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # Base extractor class
│   │   │   ├── customer_extractor.py
│   │   │   ├── subscription_extractor.py
│   │   │   ├── billing_extractor.py
│   │   │   ├── payment_extractor.py
│   │   │   └── usage_extractor.py
│   │   │
│   │   ├── transformers/           # ETL transformation logic
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── customer_transformer.py
│   │   │   ├── subscription_transformer.py
│   │   │   ├── billing_transformer.py
│   │   │   ├── payment_transformer.py
│   │   │   └── usage_transformer.py
│   │   │
│   │   ├── loaders/                # Snowflake loaders
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── snowflake_loader.py
│   │   │   └── incremental_loader.py
│   │   │
│   │   ├── validators/             # Schema and data validators
│   │   │   ├── __init__.py
│   │   │   ├── schema_validator.py
│   │   │   ├── data_validator.py
│   │   │   └── quality_checks.py
│   │   │
│   │   └── utils/                  # Utilities
│   │       ├── __init__.py
│   │       ├── logging_config.py
│   │       ├── snowflake_utils.py
│   │       ├── date_utils.py
│   │       └── retry_utils.py
│   │
│   └── airflow_dags/               # Airflow DAGs
│       ├── __init__.py
│       │
│       ├── dags/
│       │   ├── __init__.py
│       │   ├── dag_customer_ingestion.py
│       │   ├── dag_subscription_ingestion.py
│       │   ├── dag_billing_ingestion.py
│       │   ├── dag_payment_ingestion.py
│       │   ├── dag_usage_ingestion.py
│       │   ├── dag_dbt_transformations.py
│       │   ├── dag_data_quality_checks.py
│       │   └── dag_analytics_refresh.py
│       │
│       ├── plugins/
│       │   ├── __init__.py
│       │   ├── operators/
│       │   │   └── snowflake_operator.py
│       │   └── sensors/
│       │       └── snowflake_sensor.py
│       │
│       └── config/
│           ├── __init__.py
│           └── dag_config.py
│
├── sql/                            # SQL scripts
│   └── snowflake/
│       ├── setup/
│       │   ├── 01_create_database.sql
│       │   ├── 02_create_schemas.sql
│       │   ├── 03_create_warehouses.sql
│       │   ├── 04_create_roles.sql
│       │   └── 05_grant_permissions.sql
│       │
│       ├── ddl/                    # Data definition
│       │   ├── bronze_tables.sql
│       │   ├── silver_tables.sql
│       │   └── gold_tables.sql
│       │
│       └── validation/             # Validation queries
│           ├── row_counts.sql
│           ├── data_quality.sql
│           └── metric_validation.sql
│
├── tests/                          # Automated tests
│   ├── __init__.py
│   ├── conftest.py                 # pytest fixtures
│   │
│   ├── unit/
│   │   ├── test_extractors.py
│   │   ├── test_transformers.py
│   │   ├── test_loaders.py
│   │   └── test_validators.py
│   │
│   ├── integration/
│   │   ├── test_end_to_end.py
│   │   └── test_snowflake_connection.py
│   │
│   ├── data_quality/
│   │   ├── test_bronze_quality.py
│   │   ├── test_silver_quality.py
│   │   └── test_metrics_validation.py
│   │
│   └── fixtures/
│       ├── sample_customers.json
│       ├── sample_subscriptions.json
│       ├── sample_invoices.json
│       ├── sample_payments.json
│       └── sample_product_usage.json
│
├── powerbi/                        # Power BI resources
│   ├── dashboards/
│   │   ├── Executive_SaaS_Overview.pbix
│   │   ├── Revenue_Analytics.pbix
│   │   ├── Customer_Analytics.pbix
│   │   └── Subscription_Analytics.pbix
│   │
│   ├── queries/
│   │   └── power_query_templates.pq
│   │
│   └── dax_measures/
│       └── saas_metrics_library.dax
│
├── terraform/                      # Infrastructure as Code
│   ├── variables.tf
│   ├── main.tf
│   ├── snowflake.tf
│   ├── airflow.tf
│   └── terraform.tfvars.example
│
├── docker/                         # Docker configurations
│   ├── docker-compose.yml          # Local dev environment
│   ├── airflow/
│   │   └── Dockerfile
│   └── snowflake/
│       └── Dockerfile
│
├── .github/
│   └── workflows/
│       ├── ci_dbt.yml
│       ├── ci_python.yml
│       ├── ci_sql.yml
│       └── deploy.yml
│
└── .gitignore                      # Git ignore rules
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** (3.11 recommended)
- **Git**
- **Docker & Docker Compose** (for Airflow)
- **Snowflake Account** (free trial available)
- **Power BI Desktop** (Windows or Mac)
- **dbt CLI** (or use dbt Cloud)

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/saas-analytics-platform.git
cd saas-analytics-platform
```

### 2. Set Up Environment

#### Option A: Windows (Local Setup)

See **[Windows Setup Guide](./docs/setup_guides/windows_setup.md)**

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env with your Snowflake credentials
```

#### Option B: Docker (Recommended)

See **[Docker Setup Guide](./docs/setup_guides/docker_setup.md)**

```bash
docker-compose up -d

# Airflow available at http://localhost:8080
# Default credentials: airflow/airflow
```

### 3. Configure Snowflake

1. Create a Snowflake account (free trial)
2. Run setup scripts: **[Snowflake Setup Guide](./docs/setup_guides/snowflake_setup.md)**

```bash
cd sql/snowflake/setup
# Execute scripts in order: 01_*, 02_*, 03_*, 04_*, 05_*
```

### 4. Configure dbt

See **[dbt Setup Guide](./docs/setup_guides/dbt_setup.md)**

```bash
cd dbt_project

# Create profiles.yml
dbt debug

# Test connection
dbt deps
dbt parse
```

### 5. Generate Synthetic Data & Ingest

```python
# From repository root
python src/ingestion/generate_synthetic_data.py --config config/dev/config.yaml

# Run ingestion pipeline
python src/ingestion/run_ingestion.py --date 2024-01-01
```

### 6. Run dbt Transformations

```bash
cd dbt_project

dbt run --select state:new,state:modified
dbt test
dbt docs generate
dbt docs serve  # View documentation at http://localhost:8000
```

### 7. Connect Power BI

1. Open Power BI Desktop
2. Get Data → Snowflake Database
3. Load models from GOLD and ANALYTICS schemas
4. Create visualizations using provided DAX measures

---

## 📊 Data Model

### Fact Tables (GOLD Schema)

#### FactRevenue
Grain: One row per invoice line item per month

| Column | Type | Description |
|--------|------|-------------|
| revenue_key | INT | Surrogate key |
| subscription_key | INT | Foreign key to DimSubscription |
| customer_key | INT | Foreign key to DimCustomer |
| date_key | INT | Foreign key to DimDate |
| invoice_amount | DECIMAL | Invoice total |
| paid_amount | DECIMAL | Amount actually paid |
| is_recurring | BOOLEAN | Is this recurring revenue? |

#### FactSubscriptions
Grain: One row per subscription state change

| Column | Type | Description |
|--------|------|-------------|
| subscription_key | INT | Surrogate key |
| customer_key | INT | Foreign key to DimCustomer |
| date_key | INT | Foreign key to DimDate |
| product_key | INT | Foreign key to DimProduct |
| monthly_amount | DECIMAL | Monthly subscription amount |
| status | VARCHAR | active, cancelled, paused |
| action_type | VARCHAR | new, upgrade, downgrade, renewal, cancel |

### Dimension Tables (GOLD Schema)

#### DimCustomer (SCD Type 2)
Tracks customer changes over time with version history

| Column | Type | Description |
|--------|------|-------------|
| customer_key | INT | Surrogate key |
| customer_id | VARCHAR | Natural key |
| customer_name | VARCHAR | |
| segment | VARCHAR | Enterprise, Mid-Market, SMB |
| country | VARCHAR | |
| valid_from | DATE | Version effective date |
| valid_to | DATE | Version expiration date |
| is_current | BOOLEAN | Current active record |

#### DimProduct
Tracks product catalog

| Column | Type | Description |
|--------|------|-------------|
| product_key | INT | Surrogate key |
| product_id | VARCHAR | Natural key |
| product_name | VARCHAR | |
| product_tier | VARCHAR | Standard, Professional, Enterprise |
| monthly_price | DECIMAL | Base monthly price |

#### DimDate
Calendar dimension for temporal analysis

| Column | Type | Description |
|--------|------|-------------|
| date_key | INT | YYYYMMDD format |
| date | DATE | Actual date |
| year | INT | 2024 |
| quarter | INT | 1-4 |
| month | INT | 1-12 |
| day_of_month | INT | 1-31 |

For complete data model documentation, see **[Data Dictionary](./docs/data_dictionary/data_model.md)**.

---

## 📈 Business Metrics

### ARR (Annual Recurring Revenue)
Sum of all monthly recurring revenue amounts multiplied by 12 for active subscriptions

**Calculation:**
```sql
ARR = SUM(monthly_subscription_amount) * 12
  WHERE subscription_status = 'active'
  AND recurring = TRUE
```

### MRR (Monthly Recurring Revenue)
Sum of monthly recurring revenue in a specific month

**Calculation:**
```sql
MRR = SUM(monthly_subscription_amount)
  WHERE subscription_status = 'active'
  AND recurring = TRUE
  AND month = CURRENT_MONTH
```

### NRR (Net Revenue Retention)
Percentage of revenue retained by existing customers, including expansion and contraction

**Calculation:**
```
NRR = (ARR_End_Period - Churn + Expansion - Contraction) / ARR_Start_Period
```

### Customer Churn Rate
Percentage of customers lost during a period

**Calculation:**
```
Churn Rate = Cancelled Customers / Customers at Period Start
```

For complete metrics definitions and calculations, see **[SaaS Metrics Guide](./docs/business_metrics/saas_metrics.md)**.

---

## ✅ Testing Strategy

### Unit Tests
Test individual Python functions and transformations

```bash
pytest tests/unit/ -v
```

### Data Quality Tests (dbt)
Automated dbt tests in SQL

```bash
cd dbt_project
dbt test
```

### Integration Tests
End-to-end pipeline tests

```bash
pytest tests/integration/ -v
```

### Metric Validation Tests
Verify calculated metrics against sample scenarios

```bash
pytest tests/data_quality/test_metrics_validation.py -v
```

### Run All Tests
```bash
pytest tests/ -v --cov=src
```

---

## 🔐 Security & Governance

### Credentials Management
- ✅ All credentials stored in `.env` files (never in Git)
- ✅ Snowflake connection pooling via SQLAlchemy
- ✅ Role-based access control (RBAC)
- ✅ Audit logging for sensitive operations

### Data Privacy
- ✅ Personally identifiable information (PII) handling
- ✅ Encryption at rest and in transit
- ✅ Row-level security (RLS) in Power BI
- ✅ Data retention policies per schema

### Data Quality
- ✅ Automated dbt tests (uniqueness, relationships, accepted values)
- ✅ Custom business rule validation
- ✅ Anomaly detection for metrics
- ✅ Reconciliation checks

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [ARCHITECTURE.md](./ARCHITECTURE.md) | System architecture and data flow diagrams |
| [Windows Setup Guide](./docs/setup_guides/windows_setup.md) | Windows local development setup |
| [Docker Setup Guide](./docs/setup_guides/docker_setup.md) | Docker and Docker Compose setup |
| [Snowflake Setup Guide](./docs/setup_guides/snowflake_setup.md) | Snowflake database initialization |
| [dbt Setup Guide](./docs/setup_guides/dbt_setup.md) | dbt project configuration |
| [Airflow Setup Guide](./docs/setup_guides/airflow_setup.md) | Airflow orchestration setup |
| [Power BI Setup Guide](./docs/setup_guides/powerbi_setup.md) | Power BI connection and dashboards |
| [Data Dictionary](./docs/data_dictionary/data_model.md) | Complete data model documentation |
| [SaaS Metrics Guide](./docs/business_metrics/saas_metrics.md) | Business metric definitions |

---

## 🛠️ Development Workflow

### 1. Create Feature Branch
```bash
git checkout -b feature/your-feature
```

### 2. Make Changes
- Python code in `src/`
- dbt models in `dbt_project/models/`
- SQL in `sql/`
- Tests in `tests/`

### 3. Validate Locally
```bash
# Run linting
pylint src/

# Run type checking
mypy src/

# Run tests
pytest tests/ -v

# dbt validation
cd dbt_project
dbt run --select state:modified
dbt test --select state:modified
```

### 4. Commit and Push
```bash
git add .
git commit -m "feat: add new transformation model"
git push origin feature/your-feature
```

### 5. Create Pull Request
- Link to related issues
- Describe changes and test results
- Request review

### 6. CI/CD Pipeline Runs
- GitHub Actions automatically runs tests
- dbt compilation validation
- Python linting and type checking
- Merge once all checks pass

---

## 📋 Development Phases

This project is organized into 10 implementation phases:

| Phase | Focus | Status |
|-------|-------|--------|
| Phase 1 | Architecture & Repository Setup | ✅ Complete |
| Phase 2 | Synthetic Data & Python Ingestion | → Next |
| Phase 3 | Snowflake Database Setup | → Next |
| Phase 4 | Bronze, Silver, Gold Layers | → Next |
| Phase 5 | dbt Transformations | → Next |
| Phase 6 | SaaS Metrics | → Next |
| Phase 7 | Power BI Dashboards | → Next |
| Phase 8 | Airflow Orchestration | → Next |
| Phase 9 | Testing & CI/CD | → Next |
| Phase 10 | Documentation & Validation | → Next |

---

## 🤔 FAQ

**Q: Can I use this without Snowflake?**  
A: This platform is designed for Snowflake but can be adapted for PostgreSQL, BigQuery, or other warehouses.

**Q: Do I need Power BI?**  
A: Power BI is recommended for dashboards, but Looker, Tableau, or other BI tools work with minor adjustments.

**Q: How much does Snowflake cost?**  
A: Snowflake offers a free trial with $400 credits. The platform is designed for cost optimization.

**Q: Can I deploy this to production?**  
A: Yes, see [Terraform configurations](./terraform/) for infrastructure-as-code deployment.

---

## 🤝 Contributing

1. Create a feature branch
2. Make changes following the development workflow
3. Run tests and validation
4. Submit pull request with clear description

---

## 📄 License

This project is provided as-is for educational and demonstration purposes.

---

## 📞 Support & Questions

For issues, questions, or discussions:
1. Create a GitHub Issue
2. Include error logs and reproduction steps
3. Reference relevant documentation

---

## 🎯 Key Competencies Demonstrated

✅ Snowflake data warehouse design and optimization  
✅ dbt transformation pipelines and testing  
✅ Medallion architecture implementation  
✅ Dimensional modeling and star schemas  
✅ Python data ingestion and ETL  
✅ Apache Airflow orchestration  
✅ Power BI dashboards and DAX  
✅ SQL query optimization  
✅ Data quality and governance  
✅ Git-based CI/CD workflows  
✅ Cloud infrastructure concepts  
✅ Production-ready code patterns  

---

**Last Updated:** November 2024  
**Version:** 1.0.0  
**Status:** Phase 1 - Architecture Complete ✅
# saas-analytics-platform
# saas-analytics-platform
