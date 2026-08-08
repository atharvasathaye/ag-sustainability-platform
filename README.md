# Agricultural Sustainability Reporting Platform

This repository contains the data engineering and analytics code for an agricultural sustainability reporting platform. It joins USDA NASS livestock/dairy data against EPA GHG Inventory emissions factors, modeled into a producer-level star schema. 

## Key Features
- **Databricks Ingestion & Transformation**: PySpark and SQL scripts to clean, model, and prepare data.
- **Data Model**: Producer-level star schema optimized for reporting.
- **Power BI Integration**: RLS (Row-Level Security) configured so producers see only their own operation and regional teams see their region.
- **Automated Data Verification**: Workflows that quarantine anomalous records.

## Structure
- `data/` - Mock datasets representing USDA and EPA sources.
- `src/` - Databricks PySpark/SQL transformation scripts.
- `powerbi/` - Power BI template, DAX logic, and RLS configurations.
- `docs/` - Process documentation and business rules.
