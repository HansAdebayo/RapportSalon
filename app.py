import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="Dashboard Salons", layout="wide")

with st.container():
    st.markdown("<div style='max-width: 700px; margin: auto;'>", unsafe_allow_html=True)
    st.title("🎯 Tableau de bord des Salons")

    # Chargement des données
    df = pd.read_csv("salon_ok.csv")

    # === Sélection des salons ===
    st.subheader("🎯 Sélection des salons")
    evenements = sorted(df["evenement"].dropna().unique())
    all_selected = st.checkbox("Tout sélectionner", value=True)

    if all_selected:
        selection = st.multiselect("Salons sélectionnés :", evenements, default=evenements)
    else:
        selection = st.multiselect("Salons sélectionnés :", evenements)

    data = df[df["evenement"].isin(selection)]

    # === Calculs statistiques ===
    nb_leads = data["id_lead"].nunique()
    nb_abandons = data["Date_Abandon"].notna().sum()
    nb_offres = data["Date_signature_offre"].notna().sum()
    nb_pdb = data["Date_signature_pdb"].notna().sum()
    nb_qualifies = data["Date_qualification"].notna().sum()

    p_leads = data["PuissanceTotale"].sum()
    p_abandons = data.loc[data["Date_Abandon"].notna(), "PuissanceTotale"].sum()
    p_offres = data.loc[data["Date_signature_offre"].notna(), "PuissanceTotale"].sum()
    p_pdb = data.loc[data["Date_signature_pdb"].notna(), "PuissanceTotale"].sum()

    # === Affichage des KPI ===
    st.subheader("🔢 Statistiques principales")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Nombre de Leads", nb_leads, f"{p_leads:.2f} kW")
    col2.metric("Abandons", nb_abandons, f"{p_abandons:.2f} kW")
    col3.metric("Offres signées", nb_offres, f"{p_offres:.2f} kW")
    col4.metric("PDB signées", nb_pdb, f"{p_pdb:.2f} kW")

    # === Diagramme circulaire ===
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

    # === Taux de conversion classiques ===
    taux_q_to_o = round((nb_offres / nb_qualifies) * 100, 2) if nb_qualifies else 0
    taux_o_to_pdb = round((nb_pdb / nb_offres) * 100, 2) if nb_offres else 0

    st.subheader("📈 Taux de conversion")
    col5, col6 = st.columns(2)
    col5.metric("Qualification → Offre", f"{taux_q_to_o} %")
    col6.metric("Offre → PDB", f"{taux_o_to_pdb} %")

    # === Taux d'abandons à chaque étape ===
    taux_ab_leads = round((nb_abandons / nb_leads) * 100, 2) if nb_leads else 0
    taux_ab_qualif = round((nb_abandons / nb_qualifies) * 100, 2) if nb_qualifies else 0
    taux_ab_offres = round((nb_abandons / nb_offres) * 100, 2) if nb_offres else 0
    taux_ab_pdb = round((nb_abandons / nb_pdb) * 100, 2) if nb_pdb else 0

    st.subheader("❌ Taux d'abandons par étape")
    col7, col8, col9, col10 = st.columns(4)
    col7.metric("Abandons / Leads", f"{taux_ab_leads} %")
    col8.metric("Abandons / Qualifiés", f"{taux_ab_qualif} %")
    col9.metric("Abandons / Offres", f"{taux_ab_offres} %")
    col10.metric("Abandons / PDB", f"{taux_ab_pdb} %")

    # === Tableau des données ===
    with st.expander("🔍 Voir les données filtrées"):
        st.dataframe(data)

    st.markdown("</div>", unsafe_allow_html=True)
