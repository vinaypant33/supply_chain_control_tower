# Supply Chain Control Tower Dashboard

<p align="center">
  <img src="https://img.shields.io/badge/Project-Production%20Ready-black?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Data%20Pipeline-SSIS-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Visualization-Power%20BI-yellow?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Reporting-SSRS-red?style=for-the-badge"/>
</p>

<p align="center">
  <b>End-to-End Data Analytics System simulating a real-world Supply Chain Control Tower</b>
</p>

---

## Overview

This project simulates a **production-grade supply chain analytics system** where data flows through ETL pipelines into a centralized warehouse and is visualized through reporting and dashboards.

It combines **data engineering + analytics + automation** into a single integrated system.

---

## Problem Statement

Organizations struggle with:

* Inventory imbalance
* Stockouts and overstocking
* Supplier performance visibility
* Demand vs sales mismatch

This system provides a **centralized control tower** to monitor and optimize these areas.

---

# Schema

<p align="center">
  <img src="https://github.com/vinaypant33/supply_chain_control_tower/blob/main/database/screenshots/SSMS%20Data%20Warehouse/Database%20ER%20diagram%20(crow's%20foot).png" width="800"/>
</p>

### Data Flow

```text
Raw CSV Data / Data from OLTP Database
    ↓
SSIS ETL Pipeline
    ↓
SQL Server Data Warehouse
    ↓
 Power BI Dashboard / Plotly Dash Dashboard
    ↓
Automated Execution via Task Scheduler
```

---

## Tech Stack

| Layer         | Tools                                  |
| ------------- | -------------------------------------- |
| Data Source   | CSV Files / My SQL Database            |
| ETL           | SSIS                                   |
| Database      | SQL Server                             |
| Reporting     | Power Bi , Plotly                      |
| Visualization | Power BI                               |
| Automation    | Windows Task Scheduler + Batch Scripts |
| Scripting     | Python (optional utilities) + EDA      |

---

## Dashboard Highlights

✔ Inventory Gap Analysis
✔ Supplier Profitability
✔ Demand vs Sales Insights
✔ Warehouse Contribution
✔ Interactive Filters

---

## Automation

The system is fully automated using **Windows Task Scheduler**:

### ETL Automation

* SSIS package executed via `dtexec`
* Triggered using `.bat` scripts

### Execution Flow

```text
Run_SSIS.bat → Update Warehouse → Check Dashboard
```

---

## Project Structure

```text
SUPPLY_CHAIN_CONTROL_TOWER/
│
├── api/
├── automation/
├── dashboards/
├── data/
├── database/
├── docs/
├── etl/
├── reports/
├── notebooks/
├── README.md
```

---

## Key Features

* End-to-end ETL pipeline
* Centralized data warehouse
* Automated reporting system
* Business KPI tracking
* Scalable architecture

---

## KPI Coverage

* Inventory Level
* Demand Forecast
* Sales (Units Sold)
* Profit & Profit Margin
* Stockout Indicator
* Supplier Performance

👉 Detailed explanation available in:
`docs/kpi_explanation.md`

---

##  How to Run

### 1. Setup Database

* Execute SQL scripts from `database/`

### 2. Run ETL

```bash
run_ssis.bat
```

### 3. View Dashboard

* Open Power BI file from `dashboards/`

---

## 📸 Screenshots

<p align="center">
  <img src="https://github.com/vinaypant33/supply_chain_control_tower/blob/main/dashboards/Screenshots/Dashbaord%20Screen%20-%2001%20(%20Power%20BI%20).png" width="800"/>
</p>

<p align="center">
  <img src="https://github.com/vinaypant33/supply_chain_control_tower/blob/main/database/screenshots/MY%20SQL%20Table%20Diagrams/database_with_connections.png" width="800"/>
</p>

<p align="center">
  <img src="https://github.com/vinaypant33/supply_chain_control_tower/blob/main/etl/ssis/screenshots/Full%20ETL%20Load.png" width="800"/>
</p>

<p align="center">
  <img src="https://github.com/vinaypant33/supply_chain_control_tower/blob/main/docs/Dashboard%20Screenshots/Star%20Schema%20Diagram.png" width="800"/>
</p>

---

## Business Impact

This system enables:

* Better inventory planning
* Reduced stockouts
* Improved supplier decisions
* Data-driven operations

---

## Project Highlights

✔ Combines Data Engineering + Analytics
✔ Uses industry tools (SSIS, Power BI , Plotly Dash , SQL Server)
✔ Includes automation (real-world scenario)
✔ Structured like enterprise pipeline

---

## Final Note

This project is designed to reflect **real-world enterprise data systems**, not just a dashboard.

It demonstrates how raw data can be transformed into actionable insights through a structured and automated pipeline.
