import subprocess
import os

def main():
    # Chemin vers le dossier du projet DBT
    project_path = "./dbt_project"

    # Aller dans le dossier
    os.chdir(project_path)

    # Exécuter la commande dbt run
    try:
        subprocess.run(["dbt", "run"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de dbt run : {e}")

# Permet d'exécuter le script en direct ou via Airflow
if __name__ == "__main__":
    main()
