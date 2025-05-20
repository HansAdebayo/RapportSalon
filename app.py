import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Salons", layout="centered")

# Charger les données
df = pd.read_csv("salon_ok.csv")

# --- ENTÊTE ---
st.markdown("#Dashboard des Salons")
st.markdown("Un aperçu clair de l’évolution des leads par événement.")

# --- Sélection salons ---
st.subheader("Filtres")
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
col5, col6, col_abandon = st.columns(3)

col5.metric("Qualification → Offre", f"{(nb_offres / nb_qualifies * 100):.1f} %" if nb_qualifies else "N/A")
col6.metric("Offre → PDB", f"{(nb_pdb / nb_offres * 100):.1f} %" if nb_offres else "N/A")

# Ajout du taux global d'abandon
taux_global_abandon = round((nb_abandons / nb_leads) * 100, 2) if nb_leads else 0
col_abandon.metric("Taux global d’abandon", f"{taux_global_abandon} %")


st.subheader("❌ Taux d'abandons par phase")

# Taux généraux calculés sur Derniere_Phase_Avant_Abandon
abandons_phase = filtered_df[filtered_df["Date_Abandon"].notna()]["Derniere_Phase_Avant_Abandon"].value_counts()

# On ne garde que les phases souhaitées
phases_utiles = ["Complétude Du Dossier", "Qualification", "Offre"]
taux_abandon_par_phase = {
    phase: round((abandons_phase.get(phase, 0) / nb_leads * 100), 1) if nb_leads else 0
    for phase in phases_utiles
}

# Affichage dynamique en colonnes
cols = st.columns(len(phases_utiles))
for i, phase in enumerate(phases_utiles):
    cols[i].metric(f"Abandon après {phase}", f"{taux_abandon_par_phase[phase]} %")


st.subheader("Top 10 des motifs d'abandon")

# Extraire les motifs non nuls
motifs = filtered_df[filtered_df['Date_Abandon'].notna()]['wattetco_commentairemotifdabandon']

# Compter les occurrences
top_motifs = motifs.value_counts().head(10).reset_index()
top_motifs.columns = ['Motif', 'Nombre']

# Affichage sous forme de tableau
st.table(top_motifs)



# --- DONNÉES ---
with st.expander("🔍 Voir les données filtrées"):
    st.dataframe(filtered_df)

