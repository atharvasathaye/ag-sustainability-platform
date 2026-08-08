# Agricultural Sustainability Reporting Platform

This repository contains the data engineering and analytics code for an agricultural sustainability reporting platform. It joins USDA NASS livestock/dairy data against EPA GHG Inventory emissions factors, modeled into a producer-level star schema. 

## Key Features
- **Databricks Ingestion & Transformation**: PySpark and SQL scripts to clean, model, and prepare data.
- **Data Model**: Producer-level star schema optimized for reporting.
- **Power BI Integration**: RLS (Row-Level Security) configured so producers see only their own operation and regional teams see their region.
- **Automated Data Verification**: Workflows that quarantine anomalous records.

## Data Strategy (Synthetic vs. Real-World)
To protect producer privacy while demonstrating a production-ready architecture, this repository utilizes a hybrid data approach:
*   **EPA GHG Inventory Factors:** The emissions factors reflect real-world values based on EPA guidelines for various livestock types and regions.
*   **USDA NASS Livestock Data:** The individual producer records (Farm IDs, specific head counts) are entirely **synthetic**. They were algorithmically generated to simulate a real-world dataset, complete with intentional data quality issues (e.g., missing regions, negative head counts) to test the robustness of the data verification pipeline.

## Structure
- `data/` - Datasets (synthetic producer data and EPA factors).
- `src/` - Databricks PySpark/SQL transformation scripts.
- `powerbi/` - Power BI template, DAX logic, and RLS configurations.
- `docs/` - Process documentation and business rules.
