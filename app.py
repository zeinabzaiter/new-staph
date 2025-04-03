import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Weekly MRSA/VRSA Dashboard",
    page_icon="🧫",
    layout="wide"
)

# Title
st.title("Evolution hebdomadaire des phénotypes de Staphylococcus aureus")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("weekly_staph_phenotypes.csv")
    df["Week"] = pd.to_datetime(df["Week"]).dt.date  # convertir en date uniquement
    return df

df = load_data()

# Sidebar filters
with st.sidebar:
    st.header("Filtres")

    # 🔧 Calcule les bornes de semaine
    min_week = df["Week"].min()
    max_week = df["Week"].max()

    # ✅ Slider avec types homogènes : datetime.date
    week_range = st.slider(
        "Période",
        min_value=min_week,
        max_value=max_week,
        value=(min_week, max_week),
        format="YYYY-MM-DD"
    )

    selected_phenotypes = st.multiselect(
        "Phénotypes à afficher",
        options=["MRSA", "VRSA", "Wild", "others"],
        default=["MRSA", "VRSA", "Wild"]
    )

# Filtered data
df_filtered = df[(df["Week"] >= week_range[0]) & (df["Week"] <= week_range[1])]

# Display metrics
st.subheader("Statistiques")
total_cases = df_filtered["Total"].sum()
total_mrsa = df_filtered["MRSA"].sum()
total_vrsa = df_filtered["VRSA"].sum()
total_wild = df_filtered["Wild"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total isolats", f"{total_cases}")
col2.metric("MRSA", f"{total_mrsa}")
col3.metric("VRSA", f"{total_vrsa}")
col4.metric("Wild", f"{total_wild}")

# Graph: Evolution dans le temps
st.subheader("Évolution dans le temps")
fig = px.line(
    df_filtered,
    x="Week",
    y=selected_phenotypes,
    markers=True,
    labels={"value": "Nombre de cas", "Week": "Semaine"},
    title="Évolution hebdomadaire des phénotypes"
)
fig.update_layout(legend_title_text="Phénotype")
st.plotly_chart(fig, use_container_width=True)

# Graph: Distribution stacked
st.subheader("Distribution cumulée des phénotypes")
fig_area = px.area(
    df_filtered,
    x="Week",
    y=selected_phenotypes,
    title="Distribution des phénotypes par semaine",
    labels={"value": "Nombre de cas", "Week": "Semaine"}
)
fig_area.update_layout(legend_title_text="Phénotype")
st.plotly_chart(fig_area, use_container_width=True)

# Data table
st.subheader("Données brutes")
st.dataframe(df_filtered, use_container_width=True)

st.caption("Dashboard créé avec ❤️ par ChatGPT pour l'analyse microbiologique")

