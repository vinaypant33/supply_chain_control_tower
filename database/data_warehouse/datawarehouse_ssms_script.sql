CREATE DATABASE supply_chain_dw;

use supply_chain_dw;


-- Creating dimension tables  : 
create table dbo.dim_product(
	product_key int not null primary key, 
	sku_id int,
	product_name varchar(100),
	category text
);

DROP TABLE dbo.dim_product;
GO

CREATE TABLE dbo.dim_product (
    product_key INT IDENTITY(1,1) PRIMARY KEY,
    sku_id VARCHAR(50),
    product_name NVARCHAR(100),
    category NVARCHAR(100)
);
GO

create table dbo.dim_warehouse(
	warehouse_key int primary key not null,
	warehouse_id int,
	city text,
	region text
);

create table dbo.dim_supplier( 
	supplier_key int primary key,
	supplier_id int,
	supplier_name text,
	supplier_type varchar(50)
);


create table dbo.dim_date(
	date_key int primary key,
	full_date Date
);

-- Create Fact Table : fact_supply_chain
create table fact_supply_chain(
	fact_id int primary key,
	date_key int,  
	product_key  int, 
	warehouse_key int,
	supplier_key int, 
	units_sold int,
	inventory_level int, 
	reorder_point int,
	order_qty int,
	unit_cost decimal(10 , 2),
	unit_price decimal (10 , 2),
	demand_forecast int,
	stockout_flag int,
	promotion_flag int,
	supplier_lead_time_days int
);



SELECT TABLE_SCHEMA, TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
ORDER BY TABLE_NAME;
GO


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
