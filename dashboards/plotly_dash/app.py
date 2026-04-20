from __future__ import annotations

from dash import Dash
from data_loader import load_supply_chain_data
from calculations import enrich_supply_chain_data
from layout import create_layout
from callbacks import register_callbacks


# Load and prepare data once at startup
raw_df = load_supply_chain_data()
df = enrich_supply_chain_data(raw_df)

app = Dash(__name__, suppress_callback_exceptions=True)
app.title = "Reorder Intelligence Dashboard"

app.layout = create_layout(df)

register_callbacks(app, df)

server = app.server


if __name__ == "__main__":
    app.run(debug=True)