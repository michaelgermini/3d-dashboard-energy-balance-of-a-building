import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="Dashboard 3D - Bilan énergétique",
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
        "Vue d’ensemble",
        "Chauffage",
        "Électricité",
        "Photovoltaïque",
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
        name="Bâtiment",
    )

    # Simple "panneaux solaires" plane on roof
    solar = go.Scatter3d(
        x=[0.3, 1.7, 1.7, 0.3, 0.3],
        y=[0.1, 0.1, 0.9, 0.9, 0.1],
        z=[3.01, 3.01, 3.01, 3.01, 3.01],
        mode="lines",
        line=dict(color="orange", width=6),
        name="Panneaux PV",
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


if page == "Vue d’ensemble":
    st.title("Bilan énergétique du parc immobilier")
    st.caption(
        "Depuis 2006, la Ville s’engage pour atteindre ses objectifs: 100% renouvelable en 2050, "
        "consommer moins et produire mieux."
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
            ("Chauffage (2023)", f"{chauffage_delta}%", "tendance à la baisse"),
            ("Électricité (2023)", f"{elec_delta}%", "optimisations"),
            ("Production PV", f"~{pv_prod} GWh/an", f"+{pv_centrales} centrales"),
            ("Chaufferies mazout", f"{mazout} restantes", "remplacement 3-5 ans"),
        ],
    )

    st.plotly_chart(build_building_figure(), use_container_width=True)

    st.subheader("Objectifs 2050")
    st.markdown(
        "- Sortie des énergies fossiles, raccordements aux réseaux de chaleur renouvelables.\n"
        "- Efficacité énergétique: optimiser, assainir, réguler dynamiquement.\n"
        "- Production locale: multiplier l’autoproduction PV (x2 d’ici 2025, x5 d’ici 2030)."
    )

elif page == "Chauffage":
    st.title("Chauffage")

    c1, c2, c3 = st.columns(3)
    part_gaz = get_value(kpis_df, "part_gaz_pct", "75")
    kpi_row(
        (c1, c2, c3),
        [
            ("Conso 2023", f"{chauffage_delta}%", "vs 2022"),
            ("Chaufferies mazout", f"{mazout}", "à remplacer"),
            ("Gaz (part)", f"{part_gaz}%", "des besoins"),
        ],
    )

    st.markdown(
        "- Raccordement prévu au CAD Eco Jonction (2024): étape clé vers le renouvelable.\n"
        "- Régulation dynamique: 37 immeubles équipés en 2023; économies 146'000 kWh (mi-oct → fin déc).\n"
        "- Assainissement des simples vitrages: 128 bâtiments en double vitrage, ~20% d’économie sur le chauffage."
    )

    # Estimation simple d’économies mensuelles Q4 2023
    months = ["Oct", "Nov", "Déc"]
    savings = [40_000, 50_000, 56_000]
    df = pd.DataFrame({"Mois": months, "Économies (kWh)": savings})
    st.bar_chart(df.set_index("Mois"))

    st.plotly_chart(build_building_figure(), use_container_width=True)

elif page == "Électricité":
    st.title("Électricité")

    c1, c2 = st.columns(2)
    kpi_row(
        (c1, c2),
        [
            ("Conso 2023", f"{elec_delta}%", "malgré + parc"),
            ("Sites optimisés", "+", "rénovations en cours"),
        ],
    )

    st.markdown(
        "La consommation est en baisse grâce aux rénovations et à l’optimisation des installations, "
        "malgré l’augmentation du parc immobilier."
    )

    # Courbe fictive de consommation 2022-2023
    dates = pd.date_range("2023-01-01", periods=12, freq="M")
    base_2022 = np.linspace(100, 110, 12)
    conso_2023 = base_2022 * 0.952  # -4.8%
    df = pd.DataFrame({"Date": dates, "2022 (base)": base_2022, "2023": conso_2023})
    st.line_chart(df.set_index("Date"))

elif page == "Photovoltaïque":
    st.title("Solaire photovoltaïque")

    c1, c2, c3 = st.columns(3)
    kpi_row(
        (c1, c2, c3),
        [
            ("Centrales en service", f"{pv_centrales}", "autoconsommation sur 14 sites"),
            ("Production annuelle", f"~{pv_prod} GWh", "surplus injecté"),
            ("Objectifs", "x2 (2025), x5 (2030)", "surfaces disponibles"),
        ],
    )

    st.markdown(
        "La Ville auto-consomme une partie de l’électricité produite; le surplus est injecté sur le réseau "
        "(SIG). La stratégie vise à exploiter les toitures et autres surfaces disponibles."
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
            title={"text": "Avancement objectif 2025 (x2)"},
            gauge={"axis": {"range": [0, 100]}},
            domain={"row": 0, "column": 0},
        )
    )
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=prog_2030 * 100,
            title={"text": "Avancement objectif 2030 (x5)"},
            gauge={"axis": {"range": [0, 100]}},
            domain={"row": 0, "column": 1},
        )
    )
    fig.update_layout(
        grid={"rows": 1, "columns": 2, "pattern": "independent"}, height=300, margin=dict(l=0, r=0, t=10, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)
