create database supplier_data;
use supplier_data;

-- Make the table for the dataset :  
create table raw_data_supply_chain(
row_id INT auto_increment PRIMARY KEY,
date  DATE,
sku_id varchar(50),
warehouse_id varchar(50),
supplier_id varchar(50),
region varchar(50),
units_sold int,
inventory_level int,
supplier_lead_time_days int,
reorder_point int, 
order_qty int, 
unit_cost decimal(10 , 2),
unit_price decimal(10 , 2),
promotion_flag  int,
stockout_flag int, 
demand_forecast decimal(10 , 2)
);

-- Allow to laod the data from the file  : 
SHOW VARIABLES LIKE 'secure_file_priv';

SET GLOBAL local_infile = 1;

SHOW VARIABLES LIKE 'local_infile';

-- Load the file and load the data from the csv file to the table : 
LOAD DATA LOCAL INFILE 'C:/Users/vinay/Downloads/Data Analytics Projects Final Ones/Supply Chain Control Tower/supply_chain_control_tower/data/supply_chain_dataset.csv'
INTO TABLE raw_data_supply_chain
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


-- Lets verify if the data is loaded correctly.
select * from raw_data_supply_chain;



-- Doing some basic checks from the databse : 
SELECT COUNT(*) FROM raw_data_supply_chain;

# Seleting the max values
SELECT * FROM raw_data_supply_chain LIMIT 10;

# Select Duplicates fromt the table and confirm about that : 
select Date, sku_id  , warehouse_id , supplier_id,
count(*) as duplicated_count 
from raw_data_supply_chain 
group by DATE  ,sku_id  , warehouse_id , supplier_id 
having count(*) > 1;

# First making the differernt tables from the raw dataset.

-- Operational table  : This would be for the inventory side information  : 

create table inventory_operational (
inventory_id int AUTO_INCREMENT primary key,
date Date , 
sku_id varchar(50) , 
warehouse_id varchar(50), 
region varchar(50),
inventory_level  int,
reorder_point int,
order_qty  int,
stockout_flag int,
warehouse_name varchar(100),
warehouse_city varchar(100)
); 

-- Now we will load the data from the initial raw table 

INSERT INTO inventory_operational (
    Date, 
    sku_id, 
    warehouse_id, 
    region, 
    inventory_level,
    reorder_point, 
    order_qty,
    stockout_flag
)
SELECT 
    date, 
    sku_id, 
    warehouse_id, 
    region, 
    inventory_level,
    reorder_point, 
    order_qty, 
    stockout_flag
FROM raw_data_supply_chain;

-- Sales Demand operational table : 
create table sales_demand_operational (
sales_id int AUTO_INCREMENT primary key,
date Date,
sku_id varchar(50),
warehouse_id varchar(50),
units_sold int,
demand_forecast decimal(10 , 2),
promotion_flag int, 
product_name varchar(50),
product_category varchar(100)
);

-- Now load the data from the raw table in operational table :
insert into sales_demand_operational (
Date,
sku_id,
warehouse_id,
units_sold,
demand_forecast,
promotion_flag
)
SELECT 
Date,
sku_id,
warehouse_id, 
units_sold,
demand_forecast,
promotion_flag
from raw_data_supply_chain;


-- The third table  : Supplier pricing operational table :
CREATE TABLE supplier_pricing_operational (
    supplier_price_id INT AUTO_INCREMENT PRIMARY KEY,
    Date DATE,
    SKU_ID VARCHAR(50),
    Supplier_ID VARCHAR(50),
    Supplier_Lead_Time_Days INT,
    Unit_Cost DECIMAL(10,2),
    Unit_Price DECIMAL(10,2),
    Product_Name VARCHAR(100),
    Product_Category VARCHAR(100),
    Supplier_Name VARCHAR(100),
    Supplier_Type VARCHAR(100)
);


-- Load data from raw table :
INSERT INTO supplier_pricing_operational (
    Date,
    SKU_ID,
    Supplier_ID,
    Supplier_Lead_Time_Days,
    Unit_Cost,
    Unit_Price
)
SELECT
    Date,
    SKU_ID,
    Supplier_ID,
    Supplier_Lead_Time_Days,
    Unit_Cost,
    Unit_Price
FROM raw_data_supply_chain;

-- Lets make the product master table in which we will enter the names of sku , product name product category  : 
CREATE TABLE product_master (
    SKU_ID VARCHAR(50) PRIMARY KEY,
    Product_Name VARCHAR(100),
    Product_Category VARCHAR(100)
);

INSERT INTO product_master (SKU_ID, Product_Name, Product_Category) VALUES
('SKU_1', 'Wireless Earbuds', 'Electronics'),
('SKU_2', 'Bluetooth Speaker', 'Electronics'),
('SKU_3', 'Smart Watch', 'Wearables'),
('SKU_4', 'USB Charger', 'Accessories'),
('SKU_5', 'Laptop Stand', 'Office Accessories'),
('SKU_6', 'Gaming Mouse', 'Computer Accessories'),
('SKU_7', 'Mechanical Keyboard', 'Computer Accessories'),
('SKU_8', 'Portable SSD', 'Storage Devices'),
('SKU_9', 'Noise Cancelling Headphones', 'Electronics'),
('SKU_10', 'Webcam Pro', 'Electronics'),
('SKU_11', 'Laptop Backpack', 'Bags'),
('SKU_12', 'Power Bank', 'Accessories'),
('SKU_13', 'Monitor Stand', 'Office Accessories'),
('SKU_14', 'Wireless Mouse', 'Computer Accessories'),
('SKU_15', 'Desk Lamp', 'Office Accessories'),
('SKU_16', 'Tablet Cover', 'Accessories'),
('SKU_17', 'Fitness Band', 'Wearables'),
('SKU_18', 'External Hard Drive', 'Storage Devices'),
('SKU_19', 'USB Hub', 'Accessories'),
('SKU_20', 'Portable Monitor', 'Electronics'),
('SKU_21', 'Smartphone Holder', 'Accessories'),
('SKU_22', 'Bluetooth Keyboard', 'Computer Accessories'),
('SKU_23', 'Laptop Cooling Pad', 'Computer Accessories'),
('SKU_24', 'Wireless Charger', 'Accessories'),
('SKU_25', 'HDMI Cable', 'Accessories'),
('SKU_26', 'Action Camera', 'Electronics'),
('SKU_27', 'Tripod Stand', 'Accessories'),
('SKU_28', 'Mini Projector', 'Electronics'),
('SKU_29', 'Phone Gimbal', 'Electronics'),
('SKU_30', 'Portable Printer', 'Electronics'),
('SKU_31', 'Smart Home Plug', 'Smart Home'),
('SKU_32', 'Security Camera', 'Smart Home'),
('SKU_33', 'Smart Bulb', 'Smart Home'),
('SKU_34', 'Router Device', 'Networking'),
('SKU_35', 'WiFi Extender', 'Networking'),
('SKU_36', 'Microphone Kit', 'Audio'),
('SKU_37', 'Studio Headset', 'Audio'),
('SKU_38', 'Speaker Dock', 'Audio'),
('SKU_39', 'Graphics Tablet', 'Creative Devices'),
('SKU_40', 'VR Headset', 'Electronics'),
('SKU_41', 'Docking Station', 'Computer Accessories'),
('SKU_42', 'Card Reader', 'Accessories'),
('SKU_43', 'Memory Card', 'Storage Devices'),
('SKU_44', 'Flash Drive', 'Storage Devices'),
('SKU_45', 'Portable Scanner', 'Office Devices'),
('SKU_46', 'Label Printer', 'Office Devices'),
('SKU_47', 'Digital Pen', 'Creative Devices'),
('SKU_48', 'E-Reader', 'Electronics'),
('SKU_49', 'Smart Thermostat', 'Smart Home'),
('SKU_50', 'Laptop Sleeve', 'Bags');

-- warehouse master table same like product master  : 
CREATE TABLE warehouse_master (
    Warehouse_ID VARCHAR(50) PRIMARY KEY,
    Warehouse_Name VARCHAR(100),
    Warehouse_City VARCHAR(100),
    Region VARCHAR(50)
);

INSERT INTO warehouse_master (Warehouse_ID, Warehouse_Name, Warehouse_City, Region) VALUES
('WH_1', 'Dublin Central Warehouse', 'Dublin', 'West'),
('WH_2', 'Cork Distribution Hub', 'Cork', 'South'),
('WH_3', 'Galway Fulfillment Center', 'Galway', 'West'),
('WH_4', 'Limerick Supply Hub', 'Limerick', 'South'),
('WH_5', 'Belfast Storage Center', 'Belfast', 'North');


-- Same as supplier master table  : 
CREATE TABLE supplier_master (
    Supplier_ID VARCHAR(50) PRIMARY KEY,
    Supplier_Name VARCHAR(100),
    Supplier_Type VARCHAR(100)
);


INSERT INTO supplier_master (Supplier_ID, Supplier_Name, Supplier_Type) VALUES
('SUP_1', 'Alpha Supplies Ltd', 'Electronics Supplier'),
('SUP_2', 'PrimeSource Distributors', 'General Supplier'),
('SUP_3', 'Vertex Components', 'Component Supplier'),
('SUP_4', 'NorthStar Traders', 'Wholesale Supplier'),
('SUP_5', 'Delta Retail Supply', 'Retail Supplier'),
('SUP_6', 'Everlink Logistics Supply', 'Logistics Partner'),
('SUP_7', 'BluePeak Imports', 'Import Supplier'),
('SUP_8', 'SwiftChain Distributors', 'Distribution Partner'),
('SUP_9', 'NextWave Sourcing', 'Sourcing Partner'),
('SUP_10', 'CoreLine Materials', 'Material Supplier');

/* For each type we have two tables original table which we have populated
 from the raw table and second tables in which we have added the data now we will mege them in one table */

SET SQL_SAFE_UPDATES = 0;
 
 
UPDATE sales_demand_operational s
JOIN product_master p
ON TRIM(s.SKU_ID) = TRIM(p.SKU_ID)
SET
    s.Product_Name = p.Product_Name,
    s.Product_Category = p.Product_Category;
    

UPDATE supplier_pricing_operational sp
JOIN supplier_master sm
ON TRIM(sp.Supplier_ID) = TRIM(sm.Supplier_ID)
SET
    sp.Supplier_Name = sm.Supplier_Name,
    sp.Supplier_Type = sm.Supplier_Type
WHERE sp.Supplier_Name IS NULL;
    
UPDATE inventory_operational i
JOIN warehouse_master w
ON i.warehouse_id = w.Warehouse_ID
SET
    i.Warehouse_Name = w.Warehouse_Name,
    i.Warehouse_City = w.Warehouse_City;

select * from inventory_operational;
select * from supplier_pricing_operational;
select * from sales_demand_operational;

-- Setting Foreign keys for all the table that can help us to connect the tables  : 

SELECT DISTINCT SKU_ID, Product_Name, Product_Category
FROM sales_demand_operational
LIMIT 20;
SELECT DISTINCT Warehouse_ID, Warehouse_Name, Warehouse_City
FROM inventory_operational;
SELECT DISTINCT Supplier_ID, Supplier_Name, Supplier_Type
FROM supplier_pricing_operational;


-- Just confirming that there are no orphan values in the database after merging the tables  : 
SELECT DISTINCT i.SKU_ID
FROM inventory_operational i
LEFT JOIN product_master p
ON i.SKU_ID = p.SKU_ID
WHERE p.SKU_ID IS NULL;

SELECT DISTINCT i.Warehouse_ID
FROM inventory_operational i
LEFT JOIN warehouse_master w
ON i.Warehouse_ID = w.Warehouse_ID
WHERE w.Warehouse_ID IS NULL;

SELECT DISTINCT s.SKU_ID
FROM sales_demand_operational s
LEFT JOIN product_master p
ON s.SKU_ID = p.SKU_ID
WHERE p.SKU_ID IS NULL;

SELECT DISTINCT s.Warehouse_ID
FROM sales_demand_operational s
LEFT JOIN warehouse_master w
ON s.Warehouse_ID = w.Warehouse_ID
WHERE w.Warehouse_ID IS NULL;

SELECT DISTINCT sp.SKU_ID
FROM supplier_pricing_operational sp
LEFT JOIN product_master p
ON sp.SKU_ID = p.SKU_ID
WHERE p.SKU_ID IS NULL;

SELECT DISTINCT sp.Supplier_ID
FROM supplier_pricing_operational sp
LEFT JOIN supplier_master sm
ON sp.Supplier_ID = sm.Supplier_ID
WHERE sm.Supplier_ID IS NULL;

-- Adding Foreign Keys in the table  : with the delete update rules : 

ALTER TABLE inventory_operational
ADD CONSTRAINT fk_inventory_product
FOREIGN KEY (SKU_ID) REFERENCES product_master(SKU_ID)
ON UPDATE CASCADE
ON DELETE RESTRICT,
ADD CONSTRAINT fk_inventory_warehouse
FOREIGN KEY (Warehouse_ID) REFERENCES warehouse_master(Warehouse_ID)
ON UPDATE CASCADE
ON DELETE RESTRICT;

ALTER TABLE sales_demand_operational
ADD CONSTRAINT fk_sales_product
FOREIGN KEY (SKU_ID) REFERENCES product_master(SKU_ID)
ON UPDATE CASCADE
ON DELETE RESTRICT,
ADD CONSTRAINT fk_sales_warehouse
FOREIGN KEY (Warehouse_ID) REFERENCES warehouse_master(Warehouse_ID)
ON UPDATE CASCADE
ON DELETE RESTRICT;

ALTER TABLE supplier_pricing_operational
ADD CONSTRAINT fk_supplierpricing_product
FOREIGN KEY (SKU_ID) REFERENCES product_master(SKU_ID)
ON UPDATE CASCADE
ON DELETE RESTRICT,
ADD CONSTRAINT fk_supplierpricing_supplier
FOREIGN KEY (Supplier_ID) REFERENCES supplier_master(Supplier_ID)
ON UPDATE CASCADE
ON DELETE RESTRICT;


SET GLOBAL net_read_timeout = 600;
SET GLOBAL net_write_timeout = 600;
SET GLOBAL wait_timeout = 600;
SET GLOBAL interactive_timeout = 600;

SET GLOBAL max_allowed_packet = 1073741824;


drop table if exists final_supply_chain_enriched;

-- Final Table to save as it would act as the base for the ssms and ssis 
CREATE TABLE final_supply_chain_enriched AS
SELECT
    i.date,
    i.sku_id,
    s.product_name,
    s.product_category,
    i.warehouse_id,
    i.warehouse_name,
    i.warehouse_city,
    i.region,
    sp.supplier_id,
    sp.supplier_name,
    sp.supplier_type,
    s.units_sold,
    i.inventory_level,
    sp.supplier_lead_time_days,
    i.reorder_point,
    i.order_qty,
    sp.unit_cost,
    sp.unit_price,
    s.promotion_flag,
    i.stockout_flag,
    s.demand_forecast
FROM inventory_operational i
JOIN sales_demand_operational s
    ON i.date = s.date
   AND i.sku_id = s.sku_id
   AND i.warehouse_id = s.warehouse_id
JOIN supplier_pricing_operational sp
    ON i.date = sp.date
   AND i.sku_id = sp.sku_id
LIMIT 20000;


SELECT COUNT(*) FROM final_supply_chain_enriched;
SELECT * FROM final_supply_chain_enriched LIMIT 20;


SELECT * 
FROM final_supply_chain_enriched
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/final_supply_chain_sample.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';



