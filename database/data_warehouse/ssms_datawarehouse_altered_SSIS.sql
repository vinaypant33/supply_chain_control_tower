CREATE DATABASE supply_chain_dw;
GO

USE supply_chain_dw;
GO

CREATE TABLE dbo.dim_product (
    product_key INT IDENTITY(1,1) PRIMARY KEY,
    sku_id VARCHAR(50),
    product_name NVARCHAR(100),
    category NVARCHAR(100)
);
GO

CREATE TABLE dbo.dim_warehouse (
    warehouse_key INT IDENTITY(1,1) PRIMARY KEY,
    warehouse_id VARCHAR(50),
    city NVARCHAR(100),
    region NVARCHAR(100)
);
GO

CREATE TABLE dbo.dim_supplier (
    supplier_key INT IDENTITY(1,1) PRIMARY KEY,
    supplier_id VARCHAR(50),
    supplier_name NVARCHAR(100),
    supplier_type NVARCHAR(100)
);
GO

CREATE TABLE dbo.dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE
);
GO


CREATE TABLE dbo.fact_supply_chain (
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
GO


ALTER TABLE dbo.fact_supply_chain
ADD CONSTRAINT fk_fact_product
FOREIGN KEY (product_key)
REFERENCES dbo.dim_product(product_key);
GO

ALTER TABLE dbo.fact_supply_chain
ADD CONSTRAINT fk_fact_warehouse
FOREIGN KEY (warehouse_key)
REFERENCES dbo.dim_warehouse(warehouse_key);
GO

ALTER TABLE dbo.fact_supply_chain
ADD CONSTRAINT fk_fact_supplier
FOREIGN KEY (supplier_key)
REFERENCES dbo.dim_supplier(supplier_key);
GO

ALTER TABLE dbo.fact_supply_chain
ADD CONSTRAINT fk_fact_date
FOREIGN KEY (date_key)
REFERENCES dbo.dim_date(date_key);
GO
