from __future__ import annotations

import numpy as np
import pandas as pd


def _ensure_required_columns(df: pd.DataFrame) -> None:
    required = [
        "inventory_level",
        "reorder_point",
        "demand_forecast",
        "units_sold",
        "unit_cost",
        "unit_price",
        "supplier_lead_time_days",
        "warehouse_name",
        "region",
        "category",
        "supplier_name",
        "product_name",
    ]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(
            "Missing required columns after loading data: "
            + ", ".join(missing)
        )


def enrich_supply_chain_data(df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.copy()
    _ensure_required_columns(enriched)

    # Core business fields
    enriched["inventory_gap"] = enriched["inventory_level"] - enriched["reorder_point"]
    enriched["demand_gap"] = enriched["demand_forecast"] - enriched["units_sold"]

    # Recommended order quantity
    enriched["recommended_order_qty"] = np.maximum(
        enriched["demand_forecast"] - enriched["inventory_level"], 0
    )

    # Revenue, cost, profit
    enriched["revenue"] = enriched["units_sold"] * enriched["unit_price"]
    enriched["cost"] = enriched["units_sold"] * enriched["unit_cost"]
    enriched["profit"] = enriched["revenue"] - enriched["cost"]

    # Risk logic
    conditions = [
        enriched["inventory_level"] < enriched["reorder_point"],
        (enriched["inventory_level"] >= enriched["reorder_point"])
        & (enriched["inventory_level"] < enriched["demand_forecast"]),
    ]
    choices = ["High", "Medium"]
    enriched["risk_level"] = np.select(conditions, choices, default="Low")

    # Priority score
    risk_score_map = {"High": 3, "Medium": 2, "Low": 1}
    enriched["risk_score"] = enriched["risk_level"].map(risk_score_map).fillna(1)

    enriched["priority_score"] = (
        enriched["risk_score"] * 1000
        + enriched["recommended_order_qty"] * 10
        + enriched["supplier_lead_time_days"]
    )

    # Priority label
    priority_conditions = [
        enriched["priority_score"] >= enriched["priority_score"].quantile(0.80),
        enriched["priority_score"] >= enriched["priority_score"].quantile(0.50),
    ]
    priority_choices = ["High Priority", "Medium Priority"]
    enriched["priority_label"] = np.select(
        priority_conditions,
        priority_choices,
        default="Low Priority"
    )

    return enriched


def apply_filters(
    df: pd.DataFrame,
    region: str | None = None,
    warehouse: str | None = None,
    category: str | None = None,
    supplier: str | None = None,
    risk_level: str | None = None,
) -> pd.DataFrame:
    filtered = df.copy()

    if region and region != "All":
        filtered = filtered[filtered["region"] == region]

    if warehouse and warehouse != "All":
        filtered = filtered[filtered["warehouse_name"] == warehouse]

    if category and category != "All":
        filtered = filtered[filtered["category"] == category]

    if supplier and supplier != "All":
        filtered = filtered[filtered["supplier_name"] == supplier]

    if risk_level and risk_level != "All":
        filtered = filtered[filtered["risk_level"] == risk_level]

    return filtered


def get_kpis(df: pd.DataFrame) -> dict[str, float | int]:
    at_risk_products = int((df["risk_level"] == "High").sum())
    total_recommended_order_qty = float(df["recommended_order_qty"].sum())
    high_risk_warehouses = int(
        df.loc[df["risk_level"] == "High", "warehouse_name"].nunique()
    )
    total_inventory_gap = float(df["inventory_gap"].sum())
    avg_supplier_lead_time = float(df["supplier_lead_time_days"].mean())

    return {
        "at_risk_products": at_risk_products,
        "total_recommended_order_qty": total_recommended_order_qty,
        "high_risk_warehouses": high_risk_warehouses,
        "total_inventory_gap": total_inventory_gap,
        "avg_supplier_lead_time": avg_supplier_lead_time,
    }


def get_region_options(df: pd.DataFrame) -> list[dict[str, str]]:
    values = sorted(df["region"].dropna().astype(str).unique().tolist())
    return [{"label": "All", "value": "All"}] + [{"label": v, "value": v} for v in values]


def get_warehouse_options(df: pd.DataFrame) -> list[dict[str, str]]:
    values = sorted(df["warehouse_name"].dropna().astype(str).unique().tolist())
    return [{"label": "All", "value": "All"}] + [{"label": v, "value": v} for v in values]


def get_category_options(df: pd.DataFrame) -> list[dict[str, str]]:
    values = sorted(df["category"].dropna().astype(str).unique().tolist())
    return [{"label": "All", "value": "All"}] + [{"label": v, "value": v} for v in values]


def get_supplier_options(df: pd.DataFrame) -> list[dict[str, str]]:
    values = sorted(df["supplier_name"].dropna().astype(str).unique().tolist())
    return [{"label": "All", "value": "All"}] + [{"label": v, "value": v} for v in values]


def get_risk_options() -> list[dict[str, str]]:
    values = ["All", "High", "Medium", "Low"]
    return [{"label": v, "value": v} for v in values]




def build_reorder_action_table(df: pd.DataFrame) -> pd.DataFrame:
    action_df = df.copy()

    # Only keep rows where reorder action is needed
    action_df = action_df[action_df["recommended_order_qty"] > 0].copy()

    # Sort BEFORE selecting display columns
    sort_columns = []
    ascending_order = []

    if "priority_score" in action_df.columns:
        sort_columns.append("priority_score")
        ascending_order.append(False)

    if "recommended_order_qty" in action_df.columns:
        sort_columns.append("recommended_order_qty")
        ascending_order.append(False)

    if "supplier_lead_time_days" in action_df.columns:
        sort_columns.append("supplier_lead_time_days")
        ascending_order.append(False)

    if sort_columns:
        action_df = action_df.sort_values(by=sort_columns, ascending=ascending_order)

    display_columns = [
        "product_name",
        "category",
        "warehouse_name",
        "region",
        "inventory_level",
        "reorder_point",
        "demand_forecast",
        "inventory_gap",
        "recommended_order_qty",
        "supplier_name",
        "supplier_lead_time_days",
        "risk_level",
        "priority_label",
    ]

    # Keep only columns that actually exist
    display_columns = [col for col in display_columns if col in action_df.columns]
    action_df = action_df[display_columns].copy()

    action_df = action_df.rename(
        columns={
            "product_name": "Product",
            "category": "Category",
            "warehouse_name": "Warehouse",
            "region": "Region",
            "inventory_level": "Inventory",
            "reorder_point": "Reorder Point",
            "demand_forecast": "Demand Forecast",
            "inventory_gap": "Inventory Gap",
            "recommended_order_qty": "Recommended Order Qty",
            "supplier_name": "Supplier",
            "supplier_lead_time_days": "Lead Time (Days)",
            "risk_level": "Risk Level",
            "priority_label": "Priority",
        }
    )

    return action_df