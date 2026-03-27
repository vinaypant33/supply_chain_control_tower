CREATE DATABASE supply_chain_dw;

use supply_chain_dw;


-- Dimension Tables  : 

CREATE TABLE dbo.dim_product(
    product_key INT IDENTITY(1,1) PRIMARY KEY,
    sku_id VARCHAR(50),
    product_name VARCHAR(100),
    category VARCHAR(100)
);


CREATE TABLE dbo.dim_warehouse(
    warehouse_key INT IDENTITY(1,1) PRIMARY KEY,
    warehouse_id VARCHAR(50),
    warehouse_name VARCHAR(100),
    warehouse_city VARCHAR(100),
    region VARCHAR(100)
);

CREATE TABLE dbo.dim_supplier(
    supplier_key INT IDENTITY(1,1) PRIMARY KEY,
    supplier_id VARCHAR(50),
    supplier_name VARCHAR(100),
    supplier_type VARCHAR(100)
);

CREATE TABLE dbo.dim_date(
    date_key INT PRIMARY KEY,
    full_date DATE
);



CREATE TABLE dbo.fact_supply_chain(
    fact_id INT IDENTITY(1,1) PRIMARY KEY,
    date_key INT,
    product_key INT,
    warehouse_key INT,
    supplier_key INT,
    units_sold INT,
    inventory_level INT,
    reorder_point INT,
    order_qty INT,
    unit_cost DECIMAL(10,2),
    unit_price DECIMAL(10,2),
    demand_forecast DECIMAL(10,2),
    stockout_flag INT,
    promotion_flag INT,
    supplier_lead_time_days INT
);


-- Checking the schema and the tables names that i have created

SELECT TABLE_SCHEMA, TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
ORDER BY TABLE_NAME;
GO

-- Now setting the realtions in between the tables : 

alter table fact_supply_chain
	add constraint product_contraint
	foreign key ( product_key)
	references dim_product(product_key);

alter table fact_supply_chain
	add constraint warehouse_constraint
	foreign key ( warehouse_key)
	references dim_warehouse(warehouse_key);

alter table fact_supply_chain
	add constraint supplier_constraint
	foreign key(supplier_key)
	references dim_supplier(supplier_key);

alter table fact_supply_chain
	add constraint date_constraint
	foreign key (date_key)
	references dim_date(date_key);


