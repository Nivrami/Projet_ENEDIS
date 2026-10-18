# Projet_ENEDIS — EcoScan Dashboard

Dashboard interactif de prédiction et visualisation de la performance énergétique des logements français (DPE).

> Projet réalisé dans le cadre du Master 2 SISE (Statistique et Informatique pour la Science des données).

---

## Aperçu

![Page Contexte](docs/contexte.png)
![Page Analyse](docs/analyse.png)
![Page Cartographie](docs/cartographie.png)


---

## Fonctionnalités

- **Analyse descriptive** : graphiques interactifs sur la consommation, le coût énergétique et les émissions CO2
- **Cartographie** : carte interactive des logements par classe DPE et période de construction
- **Prédiction double** :
  - Consommation énergétique (kWh/an) via régression linéaire
  - Classe DPE (A→G) via Random Forest
- **Historique** : sauvegarde des prédictions effectuées
- **Conteneurisé** : Dockerfile inclus pour un déploiement sans configuration

---

## Architecture

```
Interface               APIs Flask             Modèles ML
────────────────        ──────────────         ──────────────────
                        Port 5000         ───► Régression Linéaire
Streamlit (app.py) ────►
                        Port 5001         ───► Random Forest (DPE)
```

---

## Installation

### Prérequis

- Python 3.8+
- (Optionnel) Docker

### Lancement rapide

```bash
# Cloner le repo
git clone https://github.com/Nivrami/Projet_ENEDIS.git
cd Projet_ENEDIS

# Installer les dépendances
pip install -r ml_project/requirements.txt

# Lancer l'application
cd ml_project
streamlit run app.py
```

### Avec Docker

```bash
cd ml_project
docker-compose up --build
```

Puis ouvrir [http://localhost:8501](http://localhost:8501).

---


## Modèles

- **Régression linéaire** (consommation) : modèle, imputer et scaler sont inclus dans `ml_project/models/`.
- **Random Forest** (étiquette DPE, 152 Mo) : trop lourd pour le dépôt, il est disponible dans la
  [release v1.0](https://github.com/Nivrami/Projet_ENEDIS/releases/tag/v1.0). Le télécharger dans `ml_project/models/` :

```bash
curl -L -o ml_project/models/random_forest_dpe_final_weighted.joblib \
  https://github.com/Nivrami/Projet_ENEDIS/releases/download/v1.0/random_forest_dpe_final_weighted.joblib
```

### Réentraîner le Random Forest

1. Exécuter `notebooks/02_prediction_etiquette.ipynb`, qui produit `ml_project/data/donnees_ml_preparees.csv`.
2. Lancer `python ml_project/training/entrainement_random_forest.py`.

**Fuite de données évitée :** les variables de consommation et de coût (`conso_5_usages_ef`, `cout_total_5_usages` et leurs
variantes `_energie_n1`) servent au calcul de l'étiquette DPE elle-même. Avec elles, le modèle atteint un F1 de 0,94,
un score artificiellement élevé. Le modèle final les exclut et obtient un **F1 pondéré de 0,75**
(moyenne sur 10 entraînements, écart-type 0,0003).

---

## Structure du projet

```
Projet_ENEDIS/
├── README.md
├── docs/                          # Documentation et rapports
├── notebooks/                     # Notebooks d'exploration et modélisation
│   ├── 01_nettoyage.ipynb
│   ├── 02_prediction_etiquette.ipynb
│   ├── 03_regression_lineaire.ipynb
│   └── 04_logistic_regression.ipynb
└── ml_project/                    # Application de production
    ├── app.py                     # Point d'entrée Streamlit
    ├── config.py                  # Constantes et configuration
    ├── api_manager.py             # Gestionnaire des APIs
    ├── api_linear_regression.py   # API régression linéaire (port 5000)
    ├── api_random_forest.py       # API Random Forest (port 5001)
    ├── start_app.py               # Script de démarrage
    ├── requirements.txt
    ├── Dockerfile
    ├── models/                    # Modèles ML (Random Forest : voir la release v1.0)
    ├── training/                  # Scripts d'entraînement du Random Forest
    ├── data/                      # Données (non versionnées)
    ├── img/
    └── views/                     # Pages Streamlit
        ├── contexte.py
        ├── analyse.py
        ├── cartographie.py
        ├── prediction.py
        ├── apropos.py
        └── utils.py
```

---

## Documentation

La documentation technique et fonctionnelle est disponible dans [docs/](docs/).

---

## Équipe

- Miléna GORDIEN-PIQUET
- Marvin CURTY
- Mazilda ZEHRAOUI
