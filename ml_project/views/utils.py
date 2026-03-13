import os


RENAME_MAP = {
    "surface_habitable_logement": "surface_m2",
    "etiquette_dpe": "classe_dpe",
    "conso_5_usages_ef": "conso_energie_kwh",
}


def get_logo_path() -> str:
    """
    Retourne le chemin absolu vers le logo de l'application.

    Returns:
        Chemin vers img/Logo.png.
    """
    return os.path.join(os.path.dirname(__file__), "..", "img", "Logo.png")
