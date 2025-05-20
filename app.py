import streamlit as st
import pandas as pd
import plotly.express as px

# Titre de l'app
st.set_page_config(page_title="Dashboard Salon", layout="wide")

st.title("🎯 Tableau de bord des Salons")

# Chargement des données
df = pd.read_csv("salon_ok.csv")

# Menu de sélection de l'événement
evenements = df['evenement'].dropna().unique()
evenement_selectionne = st.selectbox("Salon :", sorted(evenements))

# Filtrage
data = df[df['evenement'] == evenement_selectionne]

# KPIs principaux
nb_leads = data.shape[0]
nb_abandons = data['Statut_Abandon'].notna().sum()
nb_offres = data['Statut_Offre'].notna().sum()
nb_pdb = data['Statut_PDB'].notna().sum()
puissance_totale = data['PuissanceTotale'].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Nombre de Leads", nb_leads, f"{puissance_totale:.2f} kW")
col2.metric("Abandons", nb_abandons, f"{data.loc[data['Statut_Abandon'].notna(), 'PuissanceTotale'].sum():.2f} kW")
col3.metric("Offres signées", nb_offres, f"{data.loc[data['Statut_Offre'].notna(), 'PuissanceTotale'].sum():.2f} kW")
col4.metric("PDB signées", nb_pdb, f"{data.loc[data['Statut_PDB'].notna(), 'PuissanceTotale'].sum():.2f} kW")

# Statuts pour camembert
statuts = {
    'Offre signée': data['Statut_Offre'].notna().sum(),
    'PDB signée': data['Statut_PDB'].notna().sum(),
    'Site Qualifiée': data['Statut_Qualification'].notna().sum(),
    'Opportunité Abandonnée': data['Statut_Abandon'].notna().sum(),
}

df_statuts = pd.DataFrame({
    'Statut': list(statuts.keys()),
    'Nombre': list(statuts.values())
})

fig = px.pie(df_statuts, values='Nombre', names='Statut', hole=0.5,
             color_discrete_sequence=px.colors.qualitative.Set1,
             title="📊 Statut des leads")
st.plotly_chart(fig, use_container_width=True)

# Taux de conversion
nb_qualifies = data['Statut_Qualification'].notna().sum()
taux_qualification_en_offre = round((nb_offres / nb_qualifies) * 100, 2) if nb_qualifies else 0
taux_offre_en_pdb = round((nb_pdb / nb_offres) * 100, 2) if nb_offres else 0

col5, col6 = st.columns(2)
col5.markdown(f"<h3>Qualification en Offre</h3><h1 style='color:red;'>{taux_qualification_en_offre} %</h1>", unsafe_allow_html=True)
col6.markdown(f"<h3>Offre en PDB</h3><h1 style='color:green;'>{taux_offre_en_pdb} %</h1>", unsafe_allow_html=True)

# Afficher les données si besoin
with st.expander("📄 Afficher les données brutes"):
    st.dataframe(data)
