from __future__ import annotations

from dash import dcc, html, dash_table
from calculations import (
    get_region_options,
    get_warehouse_options,
    get_category_options,
    get_supplier_options,
    get_risk_options,
    get_kpis,
    build_reorder_action_table,
)


def create_kpi_card(title: str, value: str, card_id: str) -> html.Div:
    return html.Div(
        className="kpi-card",
        children=[
            html.Div(title, className="kpi-title"),
            html.Div(value, id=card_id, className="kpi-value"),
        ],
    )


def create_layout(df):
    kpis = get_kpis(df)
    reorder_table_df = build_reorder_action_table(df)

    min_lt = int(df["supplier_lead_time_days"].min())
    max_lt = int(df["supplier_lead_time_days"].max())

    return html.Div(
        id="app-container",
        className="app-container light-theme",
        children=[
            dcc.Store(id="theme-store", data="light"),

            # ── Header ──────────────────────────────────────────
            html.Div(
                className="header-container",
                children=[
                    html.H1("Supply Chain Tower - Commerical Dashboard", className="main-title"),
                ],
            ),

            # ── Filters + Lead Time Slider (all in one row) ──────
            html.Div(
                className="filters-container",
                children=[
                    html.Div(className="filter-box", children=[
                        html.Label("Region"),
                        dcc.Dropdown(id="region-filter", options=get_region_options(df),
                                     value="All", clearable=False),
                    ]),
                    html.Div(className="filter-box", children=[
                        html.Label("Warehouse"),
                        dcc.Dropdown(id="warehouse-filter", options=get_warehouse_options(df),
                                     value="All", clearable=False),
                    ]),
                    html.Div(className="filter-box", children=[
                        html.Label("Category"),
                        dcc.Dropdown(id="category-filter", options=get_category_options(df),
                                     value="All", clearable=False),
                    ]),
                    html.Div(className="filter-box", children=[
                        html.Label("Supplier"),
                        dcc.Dropdown(id="supplier-filter", options=get_supplier_options(df),
                                     value="All", clearable=False),
                    ]),
                    html.Div(className="filter-box", children=[
                        html.Label("Risk Level"),
                        dcc.Dropdown(id="risk-filter", options=get_risk_options(),
                                     value="All", clearable=False),
                    ]),
                    # 6th filter: compact lead time range slider
                    html.Div(className="filter-box filter-box-slider", children=[
                        html.Label(
                            id="lead-time-slider-label",
                            children=f"Lead Time: {min_lt}–{max_lt} days",
                            className="slider-label",
                        ),
                        dcc.RangeSlider(
                            id="lead-time-slider",
                            min=min_lt,
                            max=max_lt,
                            step=1,
                            value=[min_lt, max_lt],
                            marks={min_lt: str(min_lt), max_lt: str(max_lt)},
                            tooltip={"placement": "bottom", "always_visible": False},
                            allowCross=False,
                        ),
                    ]),
                ],
            ),

            # ── KPI Cards ────────────────────────────────────────
            html.Div(
                className="kpi-grid",
                children=[
                    create_kpi_card("At Risk Products",       f"{kpis['at_risk_products']:,}",              "kpi-at-risk-products"),
                    create_kpi_card("Recommended Order Qty",  f"{kpis['total_recommended_order_qty']:,.0f}", "kpi-order-qty"),
                    create_kpi_card("High Risk Warehouses",   f"{kpis['high_risk_warehouses']:,}",           "kpi-high-risk-warehouses"),
                    create_kpi_card("Total Inventory Gap",    f"{kpis['total_inventory_gap']:,.0f}",         "kpi-inventory-gap"),
                    create_kpi_card("Avg Supplier Lead Time", f"{kpis['avg_supplier_lead_time']:.1f} days",  "kpi-lead-time"),
                ],
            ),

            # ── Row 1: Warehouse Risk + Category Demand (50/50) ──
            html.Div(
                className="chart-row two-col",
                children=[
                    html.Div(className="chart-card", children=[
                        html.H3("High-Risk Warehouses", className="chart-title"),
                        dcc.Graph(id="warehouse-risk-chart",
                                  config={"displayModeBar": False},
                                  style={"height": "230px"}),
                    ]),
                    html.Div(className="chart-card", children=[
                        html.H3("Category Demand vs Inventory", className="chart-title"),
                        dcc.Graph(id="category-demand-inventory-chart",
                                  config={"displayModeBar": False},
                                  style={"height": "230px"}),
                    ]),
                ],
            ),

            # ── Row 2: Supplier Lead Time (full width) ────────────
            html.Div(
                className="chart-row one-col",
                children=[
                    html.Div(className="chart-card", children=[
                        html.H3("Supplier Lead Time Comparison (Top 10)", className="chart-title"),
                        dcc.Graph(id="supplier-lead-time-chart",
                                  config={"displayModeBar": False},
                                  style={"height": "230px"}),
                    ]),
                ],
            ),

            # ── Reorder Action Table ──────────────────────────────
            html.Div(
                className="table-card",
                children=[
                    html.H3("Reorder Action Table", className="chart-title"),
                    dash_table.DataTable(
                        id="reorder-table",
                        columns=[{"name": c, "id": c} for c in reorder_table_df.columns],
                        data=reorder_table_df.head(50).to_dict("records"),
                        sort_action="native",
                        filter_action="native",
                        page_action="native",
                        page_size=10,
                        style_table={"overflowX": "auto"},
                        style_header={
                            "backgroundColor": "#f0f4f8",
                            "fontWeight": "700",
                            "border": "1px solid #d9e2ec",
                            "color": "#102a43",
                            "fontSize": "12px",
                            "textTransform": "uppercase",
                            "letterSpacing": "0.4px",
                        },
                        style_cell={
                            "padding": "10px 12px",
                            "fontFamily": "Inter, Arial, sans-serif",
                            "fontSize": "13px",
                            "textAlign": "left",
                            "border": "1px solid #e8eef5",
                            "backgroundColor": "#ffffff",
                            "color": "#243b53",
                            "whiteSpace": "normal",
                            "height": "auto",
                        },
                        style_data_conditional=[
                            {"if": {"filter_query": '{Risk Level} = "High"',        "column_id": "Risk Level"},            "backgroundColor": "#fff0f0", "color": "#b42318", "fontWeight": "bold"},
                            {"if": {"filter_query": '{Risk Level} = "Medium"',      "column_id": "Risk Level"},            "backgroundColor": "#fff8ec", "color": "#b54708", "fontWeight": "bold"},
                            {"if": {"filter_query": '{Priority} = "High Priority"', "column_id": "Priority"},              "backgroundColor": "#fff0f0", "color": "#b42318", "fontWeight": "bold"},
                            {"if": {"filter_query": '{Recommended Order Qty} > 0',  "column_id": "Recommended Order Qty"}, "backgroundColor": "#f0f9ff", "color": "#0b4f6c", "fontWeight": "bold"},
                            {"if": {"row_index": "odd"},                                                                   "backgroundColor": "#f9fbfd"},
                        ],
                    ),
                ],
            ),

            # ── Floating theme toggle ─────────────────────────────
            html.Button("☀️", id="theme-toggle-btn", className="theme-toggle-btn",
                        title="Toggle dark / light theme", n_clicks=0),
        ],
    )