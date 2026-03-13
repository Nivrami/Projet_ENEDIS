# 📚 Documentation Technique de l'Application : Eco Scan

## 1. 🏗️ Architecture et Composants

Cette section présente une vue d'ensemble de l'architecture de l'application. Eco Scan est une application web d'analyse et de prédiction énergétique, conteneurisée pour un déploiement fiable.

### Structure de l'Application

```bash
Projet_ENEDIS/
├── README.md
├── docs/                         # DOCUMENTATION
├── notebooks/                    # NOTEBOOKS D'EXPLORATION ET MODÉLISATION
└── ml_project/
    ├── app.py                    # POINT D'ENTRÉE PRINCIPAL
    ├── config.py                 # CONSTANTES ET CONFIGURATION
    ├── requirements.txt          # DÉPENDANCES PYTHON
    ├── api_random_forest.py      # API MODÈLE RANDOM FOREST
    ├── api_linear_regression.py  # API RÉGRESSION LINÉAIRE
    ├── api_manager.py            # GESTIONNAIRE D'APIS UNIFIÉ
    ├── docker-compose.yml        # ORCHESTRATION DOCKER
    ├── Dockerfile                # CONFIGURATION DOCKER
    ├── start_app.py              # SCRIPT DE DÉMARRAGE
    ├── models/                   # MODÈLES ML (non versionnés)
    ├── data/                     # DONNÉES BRUTES ET TRAITÉES
    │   └── df_logements.parquet  # Dataset principal
    ├── img/                      # RESSOURCES VISUELLES
    │   └── Logo.png              # Logo de l'application
    ├── views/                    # MODULES INTERFACE UTILISATEUR
    │   ├── __init__.py
    │   ├── utils.py              # UTILITAIRES PARTAGÉS
    │   ├── prediction.py         # INTERFACE PRÉDICTIONS
    │   ├── analyse.py            # STATISTIQUES DESCRIPTIVES
    │   ├── apropos.py            # DESCRIPTION PROJET
    │   ├── cartographie.py       # CARTE INTERACTIVE
    │   └── contexte.py           # CONTEXTE DU DATASET
    └── streamlit/                # CONFIGURATION STREAMLIT
        └── config.toml           # THÈME ET PARAMÈTRES
```

### Schéma Architecture

```bash
┌─────────────────────────────────────────────────┐
│                 UTILISATEUR                     │
└─────────────────────────┬───────────────────────┘
                          │
┌─────────────────────────▼───────────────────────┐
│              INTERFACE STREAMLIT                │
│                (app.py)                         │
└─────────────┬─────────────┬─────────────────────┘
              │             │
┌─────────────▼─────┐ ┌─────▼─────────────────────┐
│   GESTIONNAIRE    │ │     MODULES VUES          │
│      API          │ │  (prediction, analyse,    │
│ (api_manager.py)  │ │   cartographie, etc.)     │
└─────────┬─────────┘ └───────────────────────────┘
          │
    ┌─────┴─────────────────────────────────┐
    │                                       │
┌───▼───────────┐                   ┌───────▼─────────┐
│ RANDOM FOREST │                   │ RÉGRESSION      │
│   (API)       │                   │ LINÉAIRE (API)  │
└───────────────┘                   └─────────────────┘
```

## 2. 📦 Prérequis et Installation

Pour les instructions d'installation complètes, voir le [README](../README.md).

Les dépendances sont listées dans `ml_project/requirements.txt` et incluent : Streamlit, Flask, scikit-learn, Pandas/NumPy, joblib/pickle, Folium et Plotly.


Marvin Curty, Mazilda ZEHRAOUI, Miléna Gordien Piquet - Université Lyon 2 - Master SISE