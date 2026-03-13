import threading
import time
from api_manager import APIManager
import subprocess
import sys
import os

def start_apis():
    """Démarre les APIs en arrière-plan"""
    print("🚀 Démarrage des APIs...")
    api_manager = APIManager()
    processes = api_manager.start_apis()
    return api_manager, processes

def start_streamlit():
    """Démarre l'application Streamlit"""
    print("🌐 Démarrage de l'application Streamlit...")
    time.sleep(10)  # Attendre que les APIs soient prêtes
    subprocess.Popen(["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"])

if __name__ == "__main__":
    # Démarrer les APIs
    api_manager, processes = start_apis()
    
    # Démarrer Streamlit dans un thread séparé
    streamlit_thread = threading.Thread(target=start_streamlit, daemon=True)
    streamlit_thread.start()
    
    try:
        # Maintenir le programme en vie
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt de l'application...")
        api_manager.stop_apis()