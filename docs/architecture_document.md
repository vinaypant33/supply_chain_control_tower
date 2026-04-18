# Architecture – Supply Chain Control Tower

## 🔹 Overview

This project simulates a real-world supply chain analytics system where data is processed, stored, and visualized through multiple layers with automated execution.

---

## 🔹 Architecture Flow

```
Raw Data (CSV Files)
        ↓
SSIS ETL Pipeline
        ↓
SQL Server Data Warehouse
        ↓
Reporting Layer
   ├── SSRS (Operational Reports)
   └── Power BI (Analytical Dashboard)
        ↓
Automation Layer (Windows Task Scheduler + BAT)
```

---

## 🔹 Components Description

### 1. Data Source Layer

* Raw CSV files containing supply chain data
* Includes sales, inventory, suppliers, and warehouse data

---

### 2. ETL Layer (SSIS)

* Extracts raw data
* Transforms data (cleaning, joins, calculations)
* Loads into SQL Server warehouse

**Why SSIS:**

* Industry standard ETL tool
* Supports scalable pipelines
* Integrates well with SQL Server

---

### 3. Data Warehouse Layer (SQL Server)

* Stores processed data in structured format
* Supports analytical queries
* Acts as a single source of truth

**Design Approach:**

* Structured tables for reporting
* Optimized for read-heavy workloads

---

### 4. Reporting Layer

#### SSRS (Operational Reporting)

* Generates formatted reports (PDF/Excel)
* Used for business reporting and sharing

#### Power BI (Analytical Dashboard)

* Interactive dashboard
* Supports slicing, filtering, and drill-down analysis

---

### 5. Automation Layer

Implemented using:

* Windows Task Scheduler
* Batch (.bat) files
* dtexec (for SSIS execution)
* rs.exe (for SSRS report rendering)

**Flow:**

1. SSIS package executes via batch file
2. SQL tables are updated
3. SSRS report is triggered and exported

---

## 🔹 Scheduling Strategy

Example:

* 06:00 AM → SSIS ETL execution
* 06:10 AM → SSRS report generation

Ensures reporting always uses updated data.

---

## 🔹 Key Design Decisions

* SSIS used for ETL instead of Python to simulate enterprise workflow
* SQL Server used as central warehouse
* SSRS added for operational reporting
* Power BI used for interactive analytics
* Task Scheduler used instead of SQL Agent for portability

---

## 🔹 Outcome

The system provides:

* Automated data processing
* Centralized data storage
* Real-time analytical insights
* Scheduled reporting

This architecture closely resembles real-world data analytics pipelines used in enterprises.
