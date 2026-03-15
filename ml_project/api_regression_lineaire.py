from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
import pathlib

print("Initialisation de l'API Consommation...")

# Variables numériques à standardiser
variables_standardisees = ["hauteur_sous_plafond", "surface_habitable_logement"]

# Variables OHE/booléennes (celles qui sont 0/1 ou encodées)
data_ohe_boolean = [
    "qualite_isolation_murs",
    "etiquette_dpe",
    "periode_construction",
    "nombre_appartement_cat",
    "type_batiment_immeuble",
    "type_batiment_maison",
    "type_energie_principale_chauffage_Charbon",
    "type_energie_principale_chauffage_Fioul",
    "type_energie_principale_chauffage_Gaz (GPL/Propane/Butane)",
    "type_energie_principale_chauffage_Gaz naturel",
    "type_energie_principale_chauffage_Réseau de chauffage urbain",
    "type_energie_principale_chauffage_Électricité",
    "type_energie_n1_Charbon",
    "type_energie_n1_Fioul",
    "type_energie_n1_Gaz (GPL/Propane/Butane)",
    "type_energie_n1_Gaz naturel",
    "type_energie_n1_Réseau de chauffage urbain",
    "type_energie_n1_Électricité",
    "logement_neuf",
]

all_features = variables_standardisees + data_ohe_boolean

qualite_isolation_mapping = {
    "insuffisante": 0,
    "moyenne": 1,
    "bonne": 2,
    "très bonne": 3,
}

periode_construction_mapping = {
    "avant 1948": 0,
    "1948-1974": 1,
    "1975-1977": 2,
    "1978-1982": 3,
    "1983-1988": 4,
    "1989-2000": 5,
    "2001-2005": 6,
    "2006-2012": 7,
    "2013-2021": 8,
    "après 2021": 9,
}

nombre_app_mapping = {
    "Maison(Unitaire ou 2 à 3 logements)": 0,
    "Petit Collectif(4 à 9 logements)": 1,
    "Moyen Collectif(10 à 30 logements)": 2,
    "Grand Collectif(> 30 logements)": 3,
}

# Les valeurs de type_batiment sont déduites depuis nombre_appartement_cat :
# "Maison..." → type_batiment_maison=1, les autres → type_batiment_immeuble=1
type_batiment_mapping = {
    "Maison(Unitaire ou 2 à 3 logements)": "type_batiment_maison",
    "Petit Collectif(4 à 9 logements)": "type_batiment_immeuble",
    "Moyen Collectif(10 à 30 logements)": "type_batiment_immeuble",
    "Grand Collectif(> 30 logements)": "type_batiment_immeuble",
}

# ----------------------------------------------------
# 2. INITIALISATION ET CHARGEMENT DES ASSETS
# ----------------------------------------------------

app = Flask(__name__)

# Définition des chemins absolus (méthode robuste avec pathlib)
current_dir = pathlib.Path(__file__).parent
models_dir = current_dir / "models"
model_path = models_dir / "lr_model.pkl"
imputer_path = models_dir / "lr_imputer.pkl"
scaler_path = models_dir / "lr_scaler.pkl"

lr_model = None
lr_imputer = None
lr_scaler = None


def load_models():
    """Charge le modèle, l'imputer et le scaler depuis le dossier models/."""
    global lr_model, lr_imputer, lr_scaler
    try:
        print("Chargement du modèle de consommation...")

        if not model_path.exists():
            print(f"Fichier modèle non trouvé: {model_path}")
            return
        if not imputer_path.exists():
            print(f"Fichier imputer non trouvé: {imputer_path}")
            return
        if not scaler_path.exists():
            print(f"Fichier scaler non trouvé: {scaler_path}")
            return

        lr_model = joblib.load(model_path)
        print("Modèle de consommation chargé")

        lr_imputer = joblib.load(imputer_path)
        print("Imputer chargé")

        lr_scaler = joblib.load(scaler_path)
        print("Scaler chargé")

        print("Modele de Regression Lineaire charge avec succes sur le port 5000.")

    except Exception as e:
        print(f"ERREUR FATALE: Echec du chargement des assets (port 5000). Erreur: {e}")
        lr_model = None
        lr_imputer = None
        lr_scaler = None


print("Demarrage du chargement des modeles...")
load_models()

# ----------------------------------------------------
# 3. ROUTE DE PRÉDICTION (/predict_conso)
# ----------------------------------------------------


@app.route("/predict_conso", methods=["POST"])
def predict_conso():

    if lr_model is None:
        return (
            jsonify({"error": "Modele de Consommation non charge ou indisponible."}),
            503,
        )

    try:
        data_brute = request.get_json(force=True)
        print("Donnees recues pour prediction de consommation")
    except Exception:
        return (
            jsonify({"error": "Format JSON invalide ou manquant dans la requete."}),
            400,
        )

    # --- ÉTAPE 1 : PRÉPARATION ET CONVERSION  ---

    # Initialiser toutes les features à 0 par défaut
    data_dico = {feature: 0 for feature in all_features}

    # 1. Valeurs numériques brutes
    data_dico["hauteur_sous_plafond"] = data_brute.get("hauteur_sous_plafond", 0)
    data_dico["surface_habitable_logement"] = data_brute.get(
        "surface_habitable_logement", 0
    )

    # 2. Conversion des chaînes en indices numériques
    try:
        data_dico["qualite_isolation_murs"] = qualite_isolation_mapping[
            data_brute["qualite_isolation_murs"]
        ]
        data_dico["periode_construction"] = periode_construction_mapping[
            data_brute["periode_construction"]
        ]
        nombre_app_cat = data_brute["nombre_appartement_cat"]
        data_dico["nombre_appartement_cat"] = nombre_app_mapping[nombre_app_cat]

        # 3. Déduction du type de bâtiment depuis nombre_appartement_cat
        batiment_col = type_batiment_mapping.get(nombre_app_cat)
        if batiment_col:
            data_dico[batiment_col] = 1

        # 4. Étiquette DPE prédite (reçue de l'API DPE sur le port 5001)
        data_dico["etiquette_dpe"] = data_brute["etiquette_dpe"]
        print(f"Etiquette DPE recue: {data_brute['etiquette_dpe']}")

    except KeyError as e:
        print(f"Erreur de cle: {e}")
        return jsonify({"error": f"Cle manquante dans les donnees: {e}"}), 500

    # 5. OHE pour logement neuf/ancien
    if data_brute.get("logement") == "Neuf":
        data_dico["logement_neuf"] = 1
        print("Batiment marque comme neuf")

    # 6. OHE pour les types d'énergie
    # Les clés OHE conservent les caractères d'origine (accents, espaces, parenthèses)
    # car c'est ainsi qu'elles ont été créées lors de l'entraînement du modèle.
    energie_chauffage = data_brute.get("type_energie_principale_chauffage", "").strip()
    energie_n1 = data_brute.get("type_energie_n1", "").strip()

    if energie_chauffage:
        key = f"type_energie_principale_chauffage_{energie_chauffage}"
        if key in data_dico:
            data_dico[key] = 1
            print(f"Energie chauffage activee: {key}")
        else:
            print(f"Type d'énergie chauffage inconnu (ignoré): {energie_chauffage}")

    if energie_n1:
        key = f"type_energie_n1_{energie_n1}"
        if key in data_dico:
            data_dico[key] = 1
            print(f"Energie N1 activee: {key}")
        else:
            print(f"Type d'énergie N1 inconnu (ignoré): {energie_n1}")

    # --- ÉTAPE 2 : PRÉ-TRAITEMENT (IMPUTATION + STANDARDISATION) ---

    df_input = pd.DataFrame([data_dico])

    try:
        x_standard_input = df_input[variables_standardisees]
        x_passthrough_input = df_input[data_ohe_boolean]

        # Imputation des valeurs manquantes
        x_imputed = lr_imputer.transform(x_standard_input)

        # Standardisation
        x_scaled = lr_scaler.transform(x_imputed)

        # Reconstruction de la matrice finale
        x_final_matrix = np.hstack((x_scaled, x_passthrough_input.values))

        # --- ÉTAPE 3 : PRÉDICTION ---
        prediction_brute = lr_model.predict(x_final_matrix)[0]
        # La consommation ne peut pas être négative
        prediction_finale = max(0, prediction_brute)

        print(f"Prediction consommation: {prediction_finale:.2f} kWh/an")

        return jsonify({"conso_predite_kwh": float(f"{prediction_finale:.2f}")}), 200

    except Exception as e:
        print(f"Erreur scikit-learn/prediction : {str(e)}")
        return (
            jsonify({"error": f"Erreur interne lors de la prediction : {str(e)}"}),
            500,
        )


# ----------------------------------------------------
# 4. ROUTE DE SANTÉ
# ----------------------------------------------------


@app.route("/health", methods=["GET"])
def health_check():
    """Vérifie que l'API et tous ses assets sont prêts."""
    if lr_model is None or lr_imputer is None or lr_scaler is None:
        return (
            jsonify(
                {
                    "status": "not ready",
                    "model_loaded": lr_model is not None,
                    "imputer_loaded": lr_imputer is not None,
                    "scaler_loaded": lr_scaler is not None,
                }
            ),
            503,
        )

    return (
        jsonify(
            {
                "status": "ready",
                "model_loaded": True,
                "imputer_loaded": True,
                "scaler_loaded": True,
            }
        ),
        200,
    )


@app.route("/", methods=["GET"])
def home():
    """Route racine pour les tests de connexion."""
    return (
        jsonify(
            {
                "message": "API de Prediction de Consommation Energetique",
                "status": "running",
                "port": 5000,
            }
        ),
        200,
    )


# ----------------------------------------------------
# 5. EXÉCUTION
# ----------------------------------------------------

if __name__ == "__main__":
    print("Lancement de l'API Consommation sur le port 5000...")
    print("API prete a recevoir des requetes")
    app.run(host="0.0.0.0", port=5000, debug=False)
