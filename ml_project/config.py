# Ports des APIs Flask
PORT_API_CONSO = 5000
PORT_API_DPE = 5001

# Taille des échantillons pour chaque page
N_SAMPLE = 10000          # Page Contexte
N_SAMPLE_ANALYSE = 50000  # Page Analyse
N_MAX_POINTS = 50000      # Page Cartographie

# Seuil de filtrage des consommations aberrantes (kWh/an)
MAX_CONSO_THRESHOLD = 30000

# Facteurs de calcul énergétique
PRIX_KWH = 0.18   # €/kWh moyen
CO2_FACTOR = 0.25  # kg CO2 par kWh
