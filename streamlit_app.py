import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="3D Dashboard - Building Energy Balance",
    page_icon="⚡",
    layout="wide",
)

# Sidebar menu
st.sidebar.title("Menu")

# Data loader
@st.cache_data(show_spinner=False)
def load_kpis(csv_path: str | Path) -> pd.DataFrame:
    path = Path(csv_path)
    if not path.exists():
        return pd.DataFrame()
    try:
        df = pd.read_csv(path)
        return df
    except Exception:
        return pd.DataFrame()

kpis_df = load_kpis("data/kpis_energie.csv")

def get_value(df: pd.DataFrame, column: str, default: str) -> str:
    if df is None or df.empty or column not in df.columns:
        return default
    try:
        return str(df.iloc[-1][column])
    except Exception:
        return default
page = st.sidebar.selectbox(
    "Navigation",
    (
        "Overview",
        "Heating",
        "Electricity",
        "Photovoltaics",
    ),
)

# Shared 3D figure: simple building volume

def build_building_figure():
    # Simple cuboid representing a building
    x = [0, 2, 2, 0, 0, 2, 2, 0]
    y = [0, 0, 1, 1, 0, 0, 1, 1]
    z = [0, 0, 0, 0, 3, 3, 3, 3]

    i = [0, 0, 0, 3, 4, 4, 7, 6, 1, 2, 5, 3]
    j = [1, 3, 4, 2, 5, 7, 6, 5, 2, 6, 6, 7]
    k = [3, 1, 5, 7, 7, 6, 4, 1, 6, 3, 2, 4]

    mesh = go.Mesh3d(
        x=x, y=y, z=z,
        i=i, j=j, k=k,
        color="lightblue",
        opacity=0.4,
        flatshading=True,
        name="Building",
    )

    # Simple PV plane on roof
    solar = go.Scatter3d(
        x=[0.3, 1.7, 1.7, 0.3, 0.3],
        y=[0.1, 0.1, 0.9, 0.9, 0.1],
        z=[3.01, 3.01, 3.01, 3.01, 3.01],
        mode="lines",
        line=dict(color="orange", width=6),
        name="PV panels",
    )

    fig = go.Figure(data=[mesh, solar])
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode="data",
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=400,
    )
    return fig

# KPI helpers

def kpi_row(cols, items):
    for col, (label, value, delta) in zip(cols, items):
        col.metric(label, value, delta)


if page == "Overview":
    st.title("Energy balance of the building portfolio")
    st.caption(
        "Since 2006, the City has been committed to its goals: 100% renewable by 2050, "
        "consuming less and producing better."
    )

    c1, c2, c3, c4 = st.columns(4)
    # Values from CSV with fallbacks
    chauffage_delta = get_value(kpis_df, "conso_chauffage_delta", "-8")
    elec_delta = get_value(kpis_df, "conso_elec_delta", "-4.8")
    pv_prod = get_value(kpis_df, "pv_prod_gwh", "1.0")
    pv_centrales = get_value(kpis_df, "pv_centrales", "46")
    mazout = get_value(kpis_df, "mazout_chaufferies", "42")

    kpi_row(
        (c1, c2, c3, c4),
        [
            ("Heating (2023)", f"{chauffage_delta}%", "downward trend"),
            ("Electricity (2023)", f"{elec_delta}%", "optimizations"),
            ("PV production", f"~{pv_prod} GWh/yr", f"+{pv_centrales} plants"),
            ("Oil-fired boiler rooms", f"{mazout} remaining", "replacement in 3–5 years"),
        ],
    )

    st.plotly_chart(build_building_figure(), use_container_width=True)

    st.subheader("2050 targets")
    st.markdown(
        "- Phase out fossil fuels, connect to renewable district heating networks.\n"
        "- Energy efficiency: optimize, retrofit, and implement dynamic regulation.\n"
        "- Local production: multiply PV self-production (x2 by 2025, x5 by 2030)."
    )

elif page == "Heating":
    st.title("Heating")

    c1, c2, c3 = st.columns(3)
    chauffage_delta = get_value(kpis_df, "conso_chauffage_delta", "-8")
    mazout = get_value(kpis_df, "mazout_chaufferies", "42")
    part_gaz = get_value(kpis_df, "part_gaz_pct", "75")
    kpi_row(
        (c1, c2, c3),
        [
            ("Consumption 2023", f"{chauffage_delta}%", "vs 2022"),
            ("Oil-fired boiler rooms", f"{mazout}", "to be replaced"),
            ("Gas (share)", f"{part_gaz}%", "of heat needs"),
        ],
    )

    st.markdown(
        "- Connection to CAD Eco Jonction (2024): a key step toward renewables.\n"
        "- Dynamic regulation: 37 buildings equipped in 2023; 146,000 kWh saved (mid-Oct → end-Dec).\n"
        "- Single glazing retrofit: 128 buildings upgraded to double glazing, ~20% heating savings."
    )

    # Estimation simple d’économies mensuelles Q4 2023
    months = ["Oct", "Nov", "Dec"]
    savings = [40_000, 50_000, 56_000]
    df = pd.DataFrame({"Month": months, "Savings (kWh)": savings})
    st.bar_chart(df.set_index("Month"))

    st.plotly_chart(build_building_figure(), use_container_width=True)

elif page == "Electricity":
    st.title("Electricity")

    c1, c2 = st.columns(2)
    elec_delta = get_value(kpis_df, "conso_elec_delta", "-4.8")
    kpi_row(
        (c1, c2),
        [
            ("Consumption 2023", f"{elec_delta}%", "despite larger portfolio"),
            ("Optimized sites", "+", "renovations in progress"),
        ],
    )

    st.markdown(
        "Consumption is decreasing thanks to renovations and system optimizations, "
        "despite the growing building portfolio."
    )

    # Courbe fictive de consommation 2022-2023
    dates = pd.date_range("2023-01-01", periods=12, freq="M")
    base_2022 = np.linspace(100, 110, 12)
    conso_2023 = base_2022 * 0.952  # -4.8%
    df = pd.DataFrame({"Date": dates, "2022 (baseline)": base_2022, "2023": conso_2023})
    st.line_chart(df.set_index("Date"))

elif page == "Photovoltaics":
    st.title("Solar photovoltaics")

    c1, c2, c3 = st.columns(3)
    pv_centrales = get_value(kpis_df, "pv_centrales", "46")
    pv_prod = get_value(kpis_df, "pv_prod_gwh", "1.0")
    kpi_row(
        (c1, c2, c3),
        [
            ("Plants in service", f"{pv_centrales}", "self-consumption on 14 sites"),
            ("Annual production", f"~{pv_prod} GWh", "surplus injected"),
            ("Targets", "x2 (2025), x5 (2030)", "available surfaces"),
        ],
    )

    st.markdown(
        "The City self-consumes part of the electricity produced; any surplus is injected into the grid "
        "(SIG). The strategy aims to leverage rooftops and other available surfaces."
    )

    # Indicateur d’avancement vers 2025 et 2030 (fictif)
    current = 1.0
    target_2025 = 2.0
    target_2030 = 5.0
    prog_2025 = current / target_2025
    prog_2030 = current / target_2030

    fig = go.Figure()
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=prog_2025 * 100,
            title={"text": "Progress toward 2025 target (x2)"},
            gauge={"axis": {"range": [0, 100]}},
            domain={"row": 0, "column": 0},
        )
    )
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=prog_2030 * 100,
            title={"text": "Progress toward 2030 target (x5)"},
            gauge={"axis": {"range": [0, 100]}},
            domain={"row": 0, "column": 1},
        )
    )
    fig.update_layout(
        grid={"rows": 1, "columns": 2, "pattern": "independent"}, height=300, margin=dict(l=0, r=0, t=10, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)
