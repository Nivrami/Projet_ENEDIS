import streamlit as st
import os
import base64
from views.utils import get_logo_path



def show_page():

    logo_path = get_logo_path()
    with open(logo_path, "rb") as f:
        logo_base64 = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <div style='text-align:center;'>
            <img src='data:image/png;base64,{logo_base64}' width='180'>
            <h1 style='color:#2ecc71; font-size:42px; font-weight:900;'>
                💡 À propos du projet DPE
            </h1>
            <p style='color:var(--text-color); font-style:italic; font-size:17px;'>
                Application interactive de visualisation et simulation de la performance énergétique des logements.
            </p>
            <hr style='border:1px solid var(--border-color); width:80%; margin:auto; margin-bottom:25px;'>
        </div>
        
        <style>
            :root {{
                --text-color: #bbbbbb;
                --text-color-secondary: #cccccc;
                --border-color: #333;
                --card-bg: rgba(255,255,255,0.05);
            }}
            
            @media (prefers-color-scheme: light) {{
                :root {{
                    --text-color: #333333;
                    --text-color-secondary: #555555;
                    --border-color: #dddddd;
                    --card-bg: rgba(0,0,0,0.05);
                }}
            }}
        </style>
    """,
        unsafe_allow_html=True,
    )

    # Présentation du projet
    st.markdown(
        """
        <p style='color:var(--text-color-secondary); text-align:justify; max-width:900px; margin:auto; line-height:1.6;'>
            Ce projet a été développé dans le cadre du module <b>Machine Learning</b> du Master SISE — 
            Statistique et Informatique pour la Science des Données à l’Université Lumière Lyon 2.
            <br><br>
            L’objectif est de proposer une application complète permettant d’explorer et de comprendre la 
            <b>performance énergétique des logements (DPE)</b> à travers différentes analyses et visualisations.
        </p>

        <div style='text-align:center; margin-top:15px;'>
            <ul style='list-style-position: inside; text-align:left; display:inline-block; color:var(--text-color-secondary); font-size:16px; line-height:1.8;'>
                <li><b>Analyse descriptive :</b> exploration statistique des variables du dataset.</li>
                <li><b>Cartographie :</b> visualisation géographique des logements selon leur classe DPE.</li>
                <li><b>Prédiction :</b> simulation de la classe énergétique et de la consommation à partir de données saisies.</li>
                <li><b>À propos :</b> présentation du projet, de l’équipe et des outils utilisés.</li>
            </ul>
        </div>

        <p style='color:var(--text-color-secondary); text-align:center; max-width:900px; margin:25px auto; line-height:1.6;'>
            Ce travail met en avant les compétences en <b>data science</b>, 
            <b>visualisation de données</b> et <b>développement d’interfaces interactives</b> avec Streamlit.
        </p>
    """,
        unsafe_allow_html=True,
    )

    # ÉQUIPE DU PROJET
    st.markdown(
        """
        <h2 style='color:#2ecc71; text-align:center; font-weight:900; margin-top:50px;'>Équipe du projet</h2>
        <hr style='width:50%; margin:auto; border:1px solid var(--border-color); margin-bottom:40px;'>
        <style>
            .team-avatar {{
                border-radius: 50%;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }}
            .team-avatar:hover {{
                transform: scale(1.08);
                box-shadow: 0 0 20px rgba(241, 196, 15, 0.4);
            }}
            .member-name {{
                color:#f1c40f; 
                font-weight:900;
                font-size:20px;
                margin-top:10px;
            }}
            .member-role {{
                color:var(--text-color-secondary);
                font-size:15px;
                line-height:1.5;
            }}
        </style>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div style='text-align:center;'>
                <img class='team-avatar' src='https://cdn-icons-png.flaticon.com/512/4140/4140048.png' width='120'>
                <div class='member-name'>Marvin Curty</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div style='text-align:center;'>
                <img class='team-avatar' src='https://cdn-icons-png.flaticon.com/512/4140/4140047.png' width='120'>
                <div class='member-name'>Mazilda Zehraoui</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div style='text-align:center;'>
                <img class='team-avatar' src='https://cdn-icons-png.flaticon.com/512/4140/4140037.png' width='120'>
                <div class='member-name'>Milena Gordien Piquet</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    # Technologies utilisées
    st.markdown(
        """
        <h2 style='color:#f39c12; text-align:center; font-weight:900; margin-top:60px;'>⚙️ Technologies utilisées</h2>
        <div style='text-align:center; margin-top:20px;'>
            <img src='https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg' width='70'>
            <img src='https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg' width='70'>
            <img src='https://cdn.jsdelivr.net/gh/devicons/devicon/icons/numpy/numpy-original.svg' width='70'>
            <img src='https://cdn.jsdelivr.net/gh/devicons/devicon/icons/plotly/plotly-original.svg' width='70'>
            <img src='https://streamlit.io/images/brand/streamlit-mark-color.png' width='70'>
        </div>
        <p style='color:var(--text-color-secondary); text-align:center; margin-top:15px;'>
            Python • Pandas • NumPy • Plotly • Streamlit
        </p>
    """,
        unsafe_allow_html=True,
    )

    # Objectifs futurs
    st.markdown(
        """
        <h2 style='color:#f1c40f; text-align:center; font-weight:900; margin-top:50px;'>Objectifs futurs</h2>
        <div style='color:var(--text-color-secondary); text-align:center; max-width:900px; margin:auto; line-height:1.6;'>
            Les prochaines évolutions d'<b>EcoScan Dashboard</b> visent à renforcer ses capacités d'analyse et d'intelligence.
            <br><br>
            <div style='text-align:left; display:inline-block;'>
                • Amélioration du modèle prédictif grâce à l'intégration de nouvelles variables issues de données ouvertes <br>
                &nbsp;&nbsp;&nbsp;(température, climat, type de chauffage).<br>
                • Actualisation automatique des données via une API pour maintenir les visualisations à jour en temps réel.<br>
                • Réentraînement du modèle lorsque de nouvelles données sont disponibles afin d'améliorer la précision des prédictions.<br>
                • Mise en ligne de la plateforme pour permettre un accès public et faciliter le partage des résultats.
            </div>
            <br><br>
            À terme, <b>EcoScan</b> ambitionne de devenir un outil intelligent et connecté, 
            capable de suivre en continu la performance énergétique des logements 
            et d'accompagner les utilisateurs dans leurs décisions.
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Liens utiles
    st.markdown(
        """
        <h2 style='color:#3498db; text-align:center; font-weight:900; margin-top:50px;'>🌐 Liens utiles</h2>
        <div style='text-align:center;'>
            <a href='https://github.com/miligp' target='_blank' 
               style='color:#f1c40f; font-size:18px; text-decoration:none; font-weight:700;'>
               🔗 GitHub - Miléna Gordien Piquet
            </a>
        </div>

        <hr style='border:1px solid var(--border-color); margin-top:50px;'>
        <p style='text-align:center; color:var(--text-color); font-size:14px; font-style:italic;'>
            Projet réalisé dans le cadre du module <b>Machine Learning</b> — Master SISE, Université Lumière Lyon 2 (2025)
        </p>
    """,
        unsafe_allow_html=True,
    )
