# Data Verification & Business Rules

This document outlines the critical data elements, business rules, and compliance procedures implemented in the Agricultural Sustainability Reporting Platform's ingestion pipeline.

## 1. Critical Data Elements (CDEs)
To accurately model emissions and ensure Row-Level Security (RLS) functions correctly, the following elements are deemed critical and must be present and valid in incoming datasets:
*   **Producer ID:** Unique identifier for the farm operation (Required for RLS).
*   **Region:** Geographic location of the operation (Required for RLS and EPA factor mapping).
*   **Livestock Type:** Species classification (Required for EPA factor mapping).
*   **Head Count:** Number of animals (Required for total emissions calculation).

## 2. Ingestion Business Rules & Data Integrity Checks
During the Databricks (PySpark simulation) ingestion phase, all incoming records are evaluated against the following rules. Records failing these checks are stripped from the main pipeline and sent to the `quarantine` zone.

*   **Rule BR-001 (Null/Empty Region):** If the `Region` field is blank or null, the record is quarantined. Reason: Cannot accurately apply regional EPA emissions factors or assign regional manager visibility.
*   **Rule BR-002 (Invalid Head Count):** If the `Head Count` is negative, zero, or a non-integer value, the record is quarantined. Reason: Total emissions calculations require a valid, positive integer to prevent skewed or negative emissions reporting.

## 3. Compliance and Remediation Procedures
*   **Monitoring:** The data verification workflow automatically monitors all data flows. Quarantined records are logged with a specific `quarantine_reason`.
*   **Remediation:** Regional Managers are responsible for reviewing quarantined records in their territory, identifying the source of the missing/invalid data (e.g., contacting the producer), and updating the source systems.
*   **Re-ingestion:** Once corrected in the source system, the records will be picked up in the next pipeline run and, upon passing the integrity checks, will be populated into the Star Schema.
