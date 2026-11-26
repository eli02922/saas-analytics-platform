# SaaS Analytics Engineering Platform - Architecture

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Data Architecture](#data-architecture)
4. [Component Details](#component-details)
5. [Technology Stack](#technology-stack)
6. [Data Flow](#data-flow)

---

## Overview

The SaaS Analytics Engineering Platform is a production-grade analytics solution designed to consolidate operational data from multiple business systems into a centralized data warehouse and transform it into business-ready analytics datasets.

**Key Objectives:**
- Consolidate data from customer management, subscriptions, billing, and usage systems
- Implement medallion architecture (Bronze → Silver → Gold)
- Calculate critical SaaS business metrics (ARR, MRR, NRR, Churn, CLV)
- Provide self-service analytics capabilities through Power BI dashboards
- Ensure data quality, governance, and security

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      DATA SOURCES (External Systems)                 │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────────────┐   │
│  │ Customer │Subscription │ Billing │ Payment  │  Product Usage   │   │
│  │   CRM    │ Management  │ System  │ Processor│  Tracking Events │   │
│  └──────────┴──────────┴──────────┴──────────┴──────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                  ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    PYTHON INGESTION LAYER                            │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  Extractors  → Transformers  → Validators  → Loaders          │  │
│  │  (APIs)         (ETL Logic)      (Schema)     (Snowflake)      │  │
│  └────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                  ↓
┌─────────────────────────────────────────────────────────────────────┐
│              APACHE AIRFLOW ORCHESTRATION                            │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  DAGs for Data Ingestion, dbt Transformations, QA Checks      │  │
│  └────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                  ↓
┌─────────────────────────────────────────────────────────────────────┐
│              SNOWFLAKE DATA WAREHOUSE                                │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────────────┐   │
│  │  BRONZE  │  SILVER  │   GOLD   │ANALYTICS│  Shared Services │   │
│  │  (Raw)   │(Cleaned) │ (Ready)  │ (Marts) │  (Metadata, Logs)│   │
│  └──────────┴──────────┴──────────┴──────────┴──────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                  ↓
┌──────────────────────────────────────────────────────────────────────┐
│                    DBT TRANSFORMATION PIPELINE                        │
│  ┌────────┬──────────────┬──────────┬────────────────────────────┐   │
│  │Staging │ Intermediate │  Marts   │  Snapshots & Incremental  │   │
│  └────────┴──────────────┴──────────┴────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
                                  ↓
┌──────────────────────────────────────────────────────────────────────┐
│                   POWER BI DASHBOARDS                                 │
│  ┌────────┬──────────┬──────────┬────────────────────────────────┐   │
│  │Executive│Revenue  │ Customer │  Subscription Analytics        │   │
│  │Overview │Analytics│Analytics │  Dashboards                    │   │
│  └────────┴──────────┴──────────┴────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Data Architecture

### Medallion Architecture Pattern

The platform implements the medallion (or lakehouse) architecture pattern:

```
SOURCE SYSTEMS
     ↓
  BRONZE (Raw)
  ├─ Purpose: Preserve original data exactly as received
  ├─ Characteristics: Immutable, timestamped, source-tracked
  ├─ Schema: Matches source systems, includes technical metadata
  └─ Retention: Long-term storage for audit and replay
     ↓
  SILVER (Cleaned & Standardized)
  ├─ Purpose: Single source of truth for normalized business entities
  ├─ Characteristics: Deduplicated, validated, standardized
  ├─ Schema: Business-oriented, enforced data types
  └─ Retention: Medium to long-term
     ↓
  GOLD (Analytics-Ready)
  ├─ Purpose: Optimized for analysis and reporting
  ├─ Characteristics: Fact/dimension tables, aggregate tables, metrics
  ├─ Schema: Star schema, dimensional model
  └─ Retention: Medium-term, refreshed regularly
     ↓
  ANALYTICS LAYER
  ├─ Power BI Dashboards
  ├─ Ad-hoc SQL Queries
  └─ Business Intelligence Reports
```

### Data Layers in Snowflake

**SAAS_ANALYTICS Database Structure:**

```
SAAS_ANALYTICS
├── RAW (Source data as-is)
│   ├── raw_customers
│   ├── raw_subscriptions
│   ├── raw_invoices
│   ├── raw_payments
│   └── raw_product_usage
│
├── BRONZE (Immutable historical archive)
│   ├── br_customers
│   ├── br_subscriptions
│   ├── br_invoices
│   ├── br_payments
│   └── br_product_usage
│
├── SILVER (Cleansed, deduplicated)
│   ├── sv_customers
│   ├── sv_subscriptions
│   ├── sv_invoices
│   ├── sv_payments
│   └── sv_product_usage
│
├── GOLD (Dimension and fact tables)
│   ├── dim_customers
│   ├── dim_products
│   ├── dim_subscriptions
│   ├── dim_date
│   ├── fct_subscriptions
│   ├── fct_revenue
│   ├── fct_payments
│   └── fct_customer_activity
│
└── ANALYTICS (Business metrics and marts)
    ├── mart_mrr
    ├── mart_arr
    ├── mart_customer_churn
    ├── mart_revenue_retention
    └── mart_customer_lifetime_value
```

---

## Component Details

### 1. Python Ingestion Layer

**Responsibility:** Extract data from source systems and load into Snowflake

**Key Features:**
- Modular extraction framework for each data source
- Schema validation and transformation logic
- Duplicate detection and deduplication
- Incremental loading support
- Comprehensive error handling and retry logic
- Logging and monitoring

**Directory Structure:**
```
src/ingestion/
├── extractors/      # Source system API clients
├── transformers/    # Data transformation logic
├── loaders/        # Snowflake loaders
├── validators/     # Schema and data validators
└── utils/          # Common utilities
```

### 2. Apache Airflow Orchestration

**Responsibility:** Schedule and monitor ingestion and transformation pipelines

**Key DAGs:**
1. `dag_customer_ingestion` - Customer CRM data
2. `dag_subscription_ingestion` - Subscription management
3. `dag_billing_ingestion` - Invoice and billing
4. `dag_payment_ingestion` - Payment transactions
5. `dag_usage_ingestion` - Product usage events
6. `dag_dbt_transformations` - dbt model execution
7. `dag_data_quality_checks` - Quality validation
8. `dag_analytics_refresh` - Analytics mart refresh

### 3. dbt Transformation Pipeline

**Responsibility:** Transform raw data through medallion layers

**Model Organization:**

```
dbt_project/models/
├── staging/
│   ├── stg_customers.sql
│   ├── stg_subscriptions.sql
│   ├── stg_invoices.sql
│   ├── stg_payments.sql
│   └── stg_product_usage.sql
│
├── intermediate/
│   ├── int_customer_subscriptions.sql
│   ├── int_subscription_revenue.sql
│   ├── int_monthly_revenue.sql
│   └── int_customer_activity.sql
│
├── marts/
│   ├── dimensions/
│   │   ├── dim_customers.sql (SCD Type 2)
│   │   ├── dim_products.sql
│   │   ├── dim_subscriptions.sql
│   │   └── dim_date.sql
│   │
│   ├── facts/
│   │   ├── fct_subscriptions.sql
│   │   ├── fct_revenue.sql
│   │   ├── fct_payments.sql
│   │   └── fct_customer_activity.sql
│   │
│   └── metrics/
│       ├── mart_mrr.sql
│       ├── mart_arr.sql
│       ├── mart_customer_churn.sql
│       ├── mart_revenue_retention.sql
│       └── mart_customer_lifetime_value.sql
│
└── snapshots/
    └── customer_history.sql (SCD Type 2)
```

### 4. Snowflake Data Warehouse

**Responsibilities:**
- Centralized data storage
- Performance optimization through clustering and indexing
- Access control and security
- Query performance monitoring

**Key Configuration:**
- **Database:** SAAS_ANALYTICS
- **Virtual Warehouses:** 
  - `COMPUTE_XS` for development
  - `COMPUTE_S` for production transformations
  - `ANALYTICS_M` for user queries
- **Replication:** Available for disaster recovery
- **Clustering Keys:** Defined on large fact tables

### 5. Power BI Dashboards

**Dashboards Included:**
1. **Executive SaaS Overview** - High-level KPIs
2. **Revenue Analytics** - Detailed revenue metrics
3. **Customer Analytics** - Customer behavior and cohorts
4. **Subscription Analytics** - Subscription lifecycle

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Data Warehouse** | Snowflake | Centralized cloud data warehouse |
| **Transformation** | dbt Core + SQL | Data transformation and testing |
| **Ingestion** | Python | API extraction and ETL logic |
| **Orchestration** | Apache Airflow | Workflow scheduling and monitoring |
| **BI & Analytics** | Power BI Desktop | Dashboard and reporting |
| **Version Control** | Git/GitHub | Source code management |
| **CI/CD** | GitHub Actions | Automated testing and deployment |
| **Infrastructure** | Docker | Local development and Airflow containerization |
| **IaC** | Terraform | Optional infrastructure provisioning |

---

## Data Flow

### End-to-End Data Flow Example: Customer Revenue Metric

```
1. EXTRACT
   Source: CRM API → Python Extractor
   ↓
2. LOAD TO BRONZE
   Load→ RAW (staging) → BRONZE (immutable)
   ↓
3. CLEANSE TO SILVER
   dbt stg_customers → sv_customers
   ↓
4. BUILD DIMENSIONS
   dbt dim_customers (with SCD Type 2 tracking)
   ↓
5. BUILD FACTS
   dbt fct_revenue (from invoice & subscription data)
   ↓
6. CALCULATE METRICS
   dbt mart_arr, mart_mrr, mart_customer_churn
   ↓
7. REFRESH BI
   Power BI pulls from GOLD/ANALYTICS schemas
   ↓
8. PUBLISH DASHBOARDS
   Executives view business metrics in real-time
   ↓
9. MONITOR & ALERT
   Data quality checks validate completeness and accuracy
```

### Incremental Load Strategy

```
First Run (Full Load):
  Extract all source records → Load to BRONZE → Transform to SILVER/GOLD

Subsequent Runs (Incremental):
  Extract records since last load (using last_modified_date)
  → Load to BRONZE with updated_at timestamp
  → Soft-delete old records (mark as inactive)
  → Transform in SILVER (merge logic)
  → Update GOLD dimensions (SCD Type 2)
  → Refresh ANALYTICS metrics
```

---

## Security & Governance

### Access Control
- Role-based access control (RBAC) in Snowflake
- Database roles: `LOADER`, `TRANSFORMER`, `ANALYST`, `ADMIN`
- Row-level security (RLS) in Power BI for multi-tenant scenarios

### Data Protection
- Encrypted credentials using environment variables
- No secrets in Git repositories
- Secure Snowflake connection pooling
- Audit logging for all data access

### Data Quality
- Automated dbt tests (uniqueness, relationships, accepted values)
- Custom business rule validations
- Reconciliation checks (source vs. warehouse totals)
- Anomaly detection for metrics

---

## Performance Optimization

### Snowflake Optimization
- **Clustering keys** on fact table join columns
- **Incremental materializations** for large models
- **Partition pruning** awareness in model design
- **Query result caching** for repeated queries

### dbt Optimization
- **Staging models as views** to reduce storage
- **Fact tables as tables** with clustering
- **Dimensions as tables** with clustering keys
- **Materialized views** for heavy aggregations

---

## Development and Deployment

### Local Development Setup
- Docker Compose for Airflow and Postgres
- Local dbt profiles for development Snowflake workspace
- Synthetic test data for validation

### CI/CD Pipeline
- Automated tests on every pull request
- dbt compilation and test validation
- Python code quality checks (lint, type checking)
- Automated deployment to production on merge

---

## Next Steps

1. ✅ **Phase 1:** Repository setup and architecture (this document)
2. → **Phase 2:** Synthetic data generation and source ingestion modules
3. → **Phase 3:** Snowflake database schema and setup
4. → **Phase 4:** Bronze, Silver, and Gold layer implementations
5. → **Phase 5:** dbt models and transformations
6. → **Phase 6:** SaaS business metrics
7. → **Phase 7:** Power BI dashboards
8. → **Phase 8:** Airflow orchestration
9. → **Phase 9:** Testing and CI/CD
10. → **Phase 10:** Final documentation

---

**Document Status:** Phase 1 - Architecture Complete  
**Last Updated:** 2024  
**Author:** Analytics Engineering Team
