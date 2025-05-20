import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Salons", layout="wide")

# Charger les données
df = pd.read_csv("salon_ok.csv")

# --- ENTÊTE ---
st.markdown("# 🎯 Dashboard des Salons")
st.markdown("Un aperçu clair de l’évolution des leads par événement.")

# --- Sélection salons ---
st.subheader("🗂️ Filtres")
evenements = sorted(df["evenement"].dropna().unique())
col_left, col_right = st.columns([1, 5])
with col_left:
    all_selected = st.checkbox("Tout sélectionner", value=True)

if all_selected:
    selected = st.multiselect("Choisir les salons :", evenements, default=evenements)
else:
    selected = st.multiselect("Choisir les salons :", evenements)

filtered_df = df[df["evenement"].isin(selected)]

# --- CALCULS ---
nb_leads = filtered_df["id_lead"].nunique()
nb_abandons = filtered_df["Date_Abandon"].notna().sum()
nb_offres = filtered_df["Date_signature_offre"].notna().sum()
nb_pdb = filtered_df["Date_signature_pdb"].notna().sum()
nb_qualifies = filtered_df["Date_qualification"].notna().sum()

p_leads = filtered_df["PuissanceTotale"].sum()
p_abandons = filtered_df.loc[filtered_df["Date_Abandon"].notna(), "PuissanceTotale"].sum()
p_offres = filtered_df.loc[filtered_df["Date_signature_offre"].notna(), "PuissanceTotale"].sum()
p_pdb = filtered_df.loc[filtered_df["Date_signature_pdb"].notna(), "PuissanceTotale"].sum()

# --- STATS GLOBALES ---
st.subheader("📊 Indicateurs principaux")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Leads", nb_leads, f"{p_leads:.1f} kW")
col2.metric("Abandons", nb_abandons, f"{p_abandons:.1f} kW")
col3.metric("Offres signées", nb_offres, f"{p_offres:.1f} kW")
col4.metric("PDB signées", nb_pdb, f"{p_pdb:.1f} kW")

# --- DONUT CHART ---
st.subheader("🧩 Répartition des statuts")
status_counts = {
    "Site Qualifiée": nb_qualifies,
    "Offre signée": nb_offres,
    "PDB signée": nb_pdb,
    "Abandonnée": nb_abandons
}
status_df = pd.DataFrame({
    "Statut": list(status_counts.keys()),
    "Valeur": list(status_counts.values())
})

fig = px.pie(status_df, names="Statut", values="Valeur", hole=0.4,
             color_discrete_sequence=px.colors.qualitative.Set3)
st.plotly_chart(fig, use_container_width=True)

# --- TAUX DE CONVERSION ---
st.subheader("📈 Taux de conversion")
col5, col6 = st.columns(2)
col5.metric("Qualification → Offre", f"{(nb_offres / nb_qualifies * 100):.1f} %" if nb_qualifies else "N/A")
col6.metric("Offre → PDB", f"{(nb_pdb / nb_offres * 100):.1f} %" if nb_offres else "N/A")

# --- TAUX D'ABANDON PAR ÉTAPE ---
st.subheader("❌ Taux d'abandons par étape")
col7, col8, col9, col10 = st.columns(4)
col7.metric("Abandon / Leads", f"{(nb_abandons / nb_leads * 100):.1f} %" if nb_leads else "N/A")
col8.metric("Abandon / Qualifiés", f"{(nb_abandons / nb_qualifies * 100):.1f} %" if nb_qualifies else "N/A")
col9.metric("Abandon / Offres", f"{(nb_abandons / nb_offres * 100):.1f} %" if nb_offres else "N/A")
col10.metric("Abandon / PDB", f"{(nb_abandons / nb_pdb * 100):.1f} %" if nb_pdb else "N/A")

# --- DONNÉES ---
with st.expander("🔍 Voir les données filtrées"):
    st.dataframe(filtered_df)

