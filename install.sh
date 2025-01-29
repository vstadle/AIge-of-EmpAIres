#!/bin/bash

# Arrêter le script si une commande échoue
set -e

# Vérification des dépendances système
echo "Mise à jour des paquets et installation de Python et Git..."
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip git

sudo apt install python3-venv

# Créez un environnement virtuel
python3 -m venv aige-env

# Activez-le
source aige-env/bin/activate  # Sur Linux/Mac

# Installez numpy dans cet environnement
pip install numpy pygame unidecode


# Clonage du dépôt
REPO_URL="https://github.com/vstadle/AIge-of-EmpAIres.git"
CLONE_DIR="AIge-of-EmpAIres Projet"

if [ -d "$CLONE_DIR" ]; then
    echo "Le dossier '$CLONE_DIR' existe déjà. Suppression..."
    rm -rf "$CLONE_DIR"
fi

echo "Clonage du dépôt..."
git clone "$REPO_URL" "$CLONE_DIR"

# Aller dans le répertoire du projet
cd "$CLONE_DIR"

echo "Installation terminée. Vous pouvez exécuter votre projet maintenant !"