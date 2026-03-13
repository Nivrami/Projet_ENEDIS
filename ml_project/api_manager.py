import subprocess
import time
import os
import sys
import socket
import threading
import requests
import signal
import logging
from typing import List, Optional
from config import PORT_API_CONSO, PORT_API_DPE

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


class APIManager:
    """Gestionnaire d'APIs optimisé pour le cloud"""

    def __init__(self, startup_timeout: int = 180, health_check_interval: int = 5):
        self.startup_timeout = startup_timeout
        self.health_check_interval = health_check_interval
        self.processes = []
        self.api_configs = [
            {
                "file": "api_linear_regression.py",
                "port": PORT_API_CONSO,
                "health_endpoint": "/health",
                "name": "API Consommation",
            },
            {
                "file": "api_random_forest.py",
                "port": PORT_API_DPE,
                "health_endpoint": "/health",
                "name": "API DPE",
            },
        ]

        # Gestion des signaux
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Gestion propre des signaux d'arrêt"""
        logger.info(f"Signal {signum} reçu, arrêt des APIs...")
        self.stop_apis()

    def is_port_in_use(self, port: int) -> bool:
        """Vérifie si un port est déjà utilisé"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                return s.connect_ex(("localhost", port)) == 0
        except Exception as e:
            logger.warning(f"Erreur vérification port {port}: {e}")
            return False

    def is_api_ready(self, port: int, endpoint: str = "/health") -> bool:
        """Vérifie si l'API est prête"""
        try:
            response = requests.get(f"http://localhost:{port}{endpoint}", timeout=10)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def start_single_api(self, api_config: dict) -> Optional[subprocess.Popen]:
        """Démarre une API spécifique"""
        try:
            api_file = api_config["file"]
            port = api_config["port"]
            api_name = api_config["name"]

            # Vérifier si le fichier existe
            if not os.path.exists(api_file):
                logger.error(f"Fichier API introuvable: {api_file}")
                return None

            logger.info(f"Démarrage de {api_name} ({api_file}) sur le port {port}...")

            # Démarrer le processus
            env = os.environ.copy()
            env["PYTHONUNBUFFERED"] = "1"

            process = subprocess.Popen(
                [sys.executable, "-u", api_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                text=True,
            )

            # Lire les sorties en temps réel
            self._start_output_reader(process, api_name)

            # Attendre le démarrage
            if self._wait_for_api_ready(port, api_config["health_endpoint"], api_name):
                logger.info(f"✅ {api_name} démarré avec succès sur le port {port}")
                return process
            else:
                logger.error(f"❌ {api_name} n'a pas démarré correctement")
                self._terminate_process(process)
                return None

        except Exception as e:
            logger.error(f"❌ Erreur démarrage {api_config['name']}: {e}")
            return None

    def _start_output_reader(self, process: subprocess.Popen, api_name: str):
        """Lit les sorties stdout/stderr en temps réel"""

        def read_output(stream, stream_name):
            try:
                for line in iter(stream.readline, ""):
                    if line.strip():
                        logger.info(f"{api_name} [{stream_name}]: {line.strip()}")
            except Exception as e:
                logger.debug(f"Fin lecture {stream_name} pour {api_name}")

        threading.Thread(
            target=read_output, args=(process.stdout, "stdout"), daemon=True
        ).start()

        threading.Thread(
            target=read_output, args=(process.stderr, "stderr"), daemon=True
        ).start()

    def _wait_for_api_ready(self, port: int, endpoint: str, api_name: str) -> bool:
        """Attend que l'API soit prête"""
        start_time = time.time()

        logger.info(f"⏳ Attente du démarrage de {api_name}...")

        while time.time() - start_time < self.startup_timeout:
            if self.is_port_in_use(port) and self.is_api_ready(port, endpoint):
                return True

            elapsed = int(time.time() - start_time)
            if elapsed % 15 == 0:  # Log toutes les 15 secondes
                logger.info(
                    f"⏳ En attente de {api_name}... {elapsed}s/{self.startup_timeout}s"
                )

            time.sleep(self.health_check_interval)

        logger.error(f"⏰ Timeout {api_name} après {self.startup_timeout}s")
        return False

    def _terminate_process(self, process: subprocess.Popen):
        """Termine un processus proprement"""
        try:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
        except Exception as e:
            logger.warning(f"Erreur arrêt processus: {e}")

    def start_apis(self) -> List[subprocess.Popen]:
        """Démarre toutes les APIs"""
        logger.info("🚀 Démarrage des APIs de prédiction...")

        self.processes = []

        for config in self.api_configs:
            if not self.is_api_ready(config["port"], config["health_endpoint"]):
                process = self.start_single_api(config)
                if process:
                    self.processes.append(process)
            else:
                logger.info(f"✅ {config['name']} est déjà en cours d'exécution")

        # Vérification finale
        ready_apis = sum(
            1
            for config in self.api_configs
            if self.is_api_ready(config["port"], config["health_endpoint"])
        )

        logger.info(
            f"🎯 Démarrage terminé: {ready_apis}/{len(self.api_configs)} APIs prêtes"
        )
        return self.processes

    def stop_apis(self):
        """Arrête tous les processus API"""
        logger.info("🛑 Arrêt de toutes les APIs...")

        for process in self.processes:
            try:
                self._terminate_process(process)
            except Exception as e:
                logger.warning(f"Erreur arrêt processus: {e}")

        self.processes = []
        logger.info("✅ Toutes les APIs ont été arrêtées")

    def get_status(self):
        """Retourne le statut des APIs"""
        status = {}
        for config in self.api_configs:
            status[config["name"]] = {
                "port": config["port"],
                "ready": self.is_api_ready(config["port"], config["health_endpoint"]),
                "file": config["file"],
            }
        return status


# Instance globale pour import facile
api_manager = APIManager()


def main():
    """Point d'entrée principal"""
    manager = APIManager()

    try:
        # Démarrer les APIs
        processes = manager.start_apis()

        if not processes:
            logger.warning("❌ Aucune API démarrée")
            return

        # Attendre indéfiniment
        logger.info(
            "✅ Toutes les APIs sont démarrées. Appuyez sur Ctrl+C pour arrêter."
        )
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("👋 Arrêt demandé par l'utilisateur")

    except Exception as e:
        logger.error(f"💥 Erreur critique: {e}")
    finally:
        manager.stop_apis()


if __name__ == "__main__":
    main()
