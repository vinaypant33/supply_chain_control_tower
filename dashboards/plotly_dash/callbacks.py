from __future__ import annotations

import pandas as pd
import plotly.express as px
from dash import Input, Output, State, html
from calculations import apply_filters, get_kpis, build_reorder_action_table

THEMES = {
    "dark": {
        "primary":   "#4a9eca",
        "secondary": "#7a8da6",
        "accent":    "#f6ad55",
        "grid":      "#1f2a44",
        "text":      "#e6edf7",
        "bg":        "#111a2b",
        "legend_bg": "rgba(17,26,43,0.8)",
    },
    "light": {
        "primary":   "#1e6091",
        "secondary": "#4a7fa5",
        "accent":    "#c05621",
        "grid":      "#e8eef5",
        "text":      "#102a43",
        "bg":        "#ffffff",
        "legend_bg": "rgba(255,255,255,0.9)",
    },
}


def _base_layout(fig, theme: str = "light", show_legend: bool = False):
    t = THEMES[theme]
    fig.update_layout(
        plot_bgcolor=t["bg"],
        paper_bgcolor=t["bg"],
        font=dict(family="Inter, Arial, sans-serif", color=t["text"], size=12),
        margin=dict(l=30, r=20, t=10, b=50),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="right", x=1,
            font=dict(color=t["text"], size=11),
            bgcolor=t["legend_bg"],
        ),
        showlegend=show_legend,
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor=t["grid"],
        tickfont=dict(color=t["text"], size=11),
        tickangle=-30,
    )
    fig.update_yaxes(
        gridcolor=t["grid"],
        zeroline=False,
        tickfont=dict(color=t["text"], size=11),
    )
    return fig


def register_callbacks(app, df: pd.DataFrame) -> None:

    # ── Theme toggle ─────────────────────────────────────────
    @app.callback(
        Output("theme-store", "data"),
        Output("app-container", "className"),
        Output("theme-toggle-btn", "children"),
        Input("theme-toggle-btn", "n_clicks"),
        State("theme-store", "data"),
        prevent_initial_call=True,
    )
    def toggle_theme(n_clicks, current_theme):
        new_theme = "light" if current_theme == "dark" else "dark"
        icon = "🌙" if new_theme == "dark" else "☀️"
        return new_theme, f"app-container {new_theme}-theme", icon

    # ── Slider label update ───────────────────────────────────
    @app.callback(
        Output("lead-time-slider-label", "children"),
        Input("lead-time-slider", "value"),
    )
    def update_slider_label(value):
        return f"Supplier Lead Time (days): {value[0]} – {value[1]}"

    # ── Main dashboard ────────────────────────────────────────
    @app.callback(
        [
            Output("kpi-at-risk-products",             "children"),
            Output("kpi-order-qty",                    "children"),
            Output("kpi-high-risk-warehouses",         "children"),
            Output("kpi-inventory-gap",                "children"),
            Output("kpi-lead-time",                    "children"),
            Output("warehouse-risk-chart",             "figure"),
            Output("category-demand-inventory-chart",  "figure"),
            Output("supplier-lead-time-chart",         "figure"),
            Output("reorder-table",                    "data"),
        ],
        [
            Input("region-filter",     "value"),
            Input("warehouse-filter",  "value"),
            Input("category-filter",   "value"),
            Input("supplier-filter",   "value"),
            Input("risk-filter",       "value"),
            Input("lead-time-slider",  "value"),
            Input("theme-store",       "data"),
        ],
    )
    def update_dashboard(region, warehouse, category, supplier, risk_level, lead_time_range, theme):
        theme = theme or "light"
        t = THEMES[theme]

        filtered_df = apply_filters(
            df=df,
            region=region,
            warehouse=warehouse,
            category=category,
            supplier=supplier,
            risk_level=risk_level,
        )

        # Apply lead time range filter
        lt_min, lt_max = lead_time_range
        filtered_df = filtered_df[
            (filtered_df["supplier_lead_time_days"] >= lt_min) &
            (filtered_df["supplier_lead_time_days"] <= lt_max)
        ]

        # ── KPIs ──────────────────────────────────────────────
        kpis = get_kpis(filtered_df)
        kpi_1 = f"{kpis['at_risk_products']:,}"
        kpi_2 = f"{kpis['total_recommended_order_qty']:,.0f}"
        kpi_3 = f"{kpis['high_risk_warehouses']:,}"
        kpi_4 = f"{kpis['total_inventory_gap']:,.0f}"
        kpi_5 = f"{kpis['avg_supplier_lead_time']:.1f} days"

        # ── Warehouse Risk ─────────────────────────────────────
        wh_df = (
            filtered_df[filtered_df["risk_level"] == "High"]
            .groupby("warehouse_name", as_index=False)
            .size()
            .rename(columns={"size": "at_risk_count"})
            .sort_values("at_risk_count", ascending=False)
        )
        if wh_df.empty:
            wh_df = (
                filtered_df.groupby("warehouse_name", as_index=False)
                .size()
                .rename(columns={"size": "at_risk_count"})
                .sort_values("at_risk_count", ascending=False)
            )
        fig_wh = px.bar(wh_df, x="warehouse_name", y="at_risk_count",
                        color_discrete_sequence=[t["secondary"]])
        fig_wh.update_traces(hovertemplate="%{x}<br>At Risk: %{y}")
        fig_wh.update_yaxes(title=None)
        fig_wh.update_xaxes(title=None)
        fig_wh = _base_layout(fig_wh, theme=theme)

        # ── Category Demand vs Inventory ───────────────────────
        cat_df = (
            filtered_df.groupby("category", as_index=False)[["demand_forecast", "inventory_level"]]
            .sum()
            .sort_values("demand_forecast", ascending=False)
        )
        cat_long = cat_df.melt(
            id_vars="category",
            value_vars=["demand_forecast", "inventory_level"],
            var_name="metric", value_name="value",
        )
        fig_cat = px.bar(
            cat_long, x="category", y="value", color="metric", barmode="group",
            color_discrete_map={"demand_forecast": t["primary"], "inventory_level": t["secondary"]},
        )
        fig_cat.update_traces(hovertemplate="%{x}<br>%{legendgroup}: %{y:,.0f}")
        fig_cat.update_yaxes(title=None)
        fig_cat.update_xaxes(title=None)
        fig_cat = _base_layout(fig_cat, theme=theme, show_legend=True)

        # ── Supplier Lead Time ─────────────────────────────────
        sup_df = (
            filtered_df.groupby("supplier_name", as_index=False)["supplier_lead_time_days"]
            .mean()
            .sort_values("supplier_lead_time_days", ascending=False)
            .head(10)
        )
        fig_sup = px.bar(sup_df, x="supplier_name", y="supplier_lead_time_days",
                         color_discrete_sequence=[t["accent"]])
        fig_sup.update_traces(hovertemplate="%{x}<br>Avg Lead Time: %{y:.1f} days")
        fig_sup.update_yaxes(title=None)
        fig_sup.update_xaxes(title=None)
        fig_sup = _base_layout(fig_sup, theme=theme)

        # ── Table ──────────────────────────────────────────────
        tbl_df = build_reorder_action_table(filtered_df)

        return (kpi_1, kpi_2, kpi_3, kpi_4, kpi_5,
                fig_wh, fig_cat, fig_sup,
                tbl_df.to_dict("records"))
