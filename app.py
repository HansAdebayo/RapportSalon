import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Salons", layout="wide")
st.title("🎯 Tableau de bord des Salons")

# Charger le fichier CSV
df = pd.read_csv("salon_ok.csv")

# Menu déroulant pour choisir l'événement
evenements = df["evenement"].dropna().unique()
evenement = st.selectbox("Salon :", sorted(evenements))

# Filtrage selon l'événement sélectionné
data = df[df["evenement"] == evenement]

# Calculs
nb_leads = data["id_lead"].nunique()
nb_abandons = data["Date_Abandon"].notna().sum()
nb_offres = data["Date_signature_offre"].notna().sum()
nb_pdb = data["Date_signature_pdb"].notna().sum()
nb_qualifies = data["Date_qualification"].notna().sum()

p_leads = data["PuissanceTotale"].sum()
p_abandons = data.loc[data["Date_Abandon"].notna(), "PuissanceTotale"].sum()
p_offres = data.loc[data["Date_signature_offre"].notna(), "PuissanceTotale"].sum()
p_pdb = data.loc[data["Date_signature_pdb"].notna(), "PuissanceTotale"].sum()

# Affichage des KPI
col1, col2, col3, col4 = st.columns(4)
col1.metric("Nombre de Leads", nb_leads, f"{p_leads:.2f} kW")
col2.metric("Abandons", nb_abandons, f"{p_abandons:.2f} kW")
col3.metric("Offres signées", nb_offres, f"{p_offres:.2f} kW")
col4.metric("PDB signées", nb_pdb, f"{p_pdb:.2f} kW")

# Graphique donut : statuts
statuts = {
    "Offre signée": nb_offres,
    "PDB signée": nb_pdb,
    "Site Qualifiée": nb_qualifies,
    "Opportunité Abandonnée": nb_abandons
}

df_statuts = pd.DataFrame({
    "Statut": list(statuts.keys()),
    "Nombre": list(statuts.values())
})

st.subheader("📊 Statut des leads")
fig = px.pie(df_statuts, names="Statut", values="Nombre", hole=0.5,
             color_discrete_sequence=px.colors.qualitative.Bold)
st.plotly_chart(fig, use_container_width=True)

# Taux de conversion
taux_q_to_o = round((nb_offres / nb_qualifies) * 100, 2) if nb_qualifies else 0
taux_o_to_pdb = round((nb_pdb / nb_offres) * 100, 2) if nb_offres else 0

col5, col6 = st.columns(2)
col5.markdown(f"<h3>Qualification en Offre</h3><h1 style='color:red;'>{taux_q_to_o} %</h1>", unsafe_allow_html=True)
col6.markdown(f"<h3>Offre en PDB</h3><h1 style='color:green;'>{taux_o_to_pdb} %</h1>", unsafe_allow_html=True)

# Affichage facultatif des données
with st.expander("🔍 Voir les données filtrées"):
    st.dataframe(data)
