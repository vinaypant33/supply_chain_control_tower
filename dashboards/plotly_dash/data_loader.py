from __future__ import annotations

from pathlib import Path
import pandas as pd


def get_data_path() -> Path:
    current_file = Path(__file__).resolve()
    project_root = current_file.parents[2]
    return project_root / "data" / "processed" / "final_supply_chain_sample.csv"


def load_supply_chain_data() -> pd.DataFrame:
    data_path = get_data_path()

    if not data_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {data_path}\n"
            "Expected file: data/processed/final_supply_chain_sample.csv"
        )

    df = pd.read_csv(data_path, header=None)


    df.columns = [
        "date",
        "sku_id",
        "product_name",
        "category",
        "warehouse_id",
        "warehouse_name",
        "warehouse_city",
        "region",
        "supplier_id",
        "supplier_name",
        "supplier_type",
        "supplier_lead_time_days",
        "inventory_level",
        "units_sold",
        "reorder_point",
        "order_quantity",
        "unit_cost",
        "unit_price",
        "promotion_flag",
        "stockout_flag",
        "demand_forecast",
    ]

    # Date parsing
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Numeric conversion
    numeric_columns = [
        "supplier_lead_time_days",
        "inventory_level",
        "units_sold",
        "reorder_point",
        "order_quantity",
        "unit_cost",
        "unit_price",
        "promotion_flag",
        "stockout_flag",
        "demand_forecast",
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Clean text columns
    text_columns = [
        "sku_id",
        "product_name",
        "category",
        "warehouse_id",
        "warehouse_name",
        "warehouse_city",
        "region",
        "supplier_id",
        "supplier_name",
        "supplier_type",
    ]

    for col in text_columns:
        df[col] = df[col].astype(str).str.strip()

    df["order_qty"] = df["order_quantity"]

    return df