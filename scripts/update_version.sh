#!/bin/bash

source venv/bin/activate

# Définir le chemin du fichier de version
VERSION_FILE="version.json"

# Vérifier si le fichier de version existe
if [ ! -f "$VERSION_FILE" ]; then
  echo "Le fichier de version '$VERSION_FILE' n'existe pas. Assurez-vous qu'il existe avant de continuer."
  exit 1
fi

# Vérifier si le paquet 'wheel' est installé
if  ! pip list | grep -q wheel ; then
    echo "Le paquet 'wheel' n'est pas installé. Installation en cours..."
    pip install wheel
else
    echo "Le paquet 'wheel' est déjà installé."
fi

# Vérifier si le paquet 'twine' est installé
if  ! pip list | grep -q twine ; then
    echo "Le paquet 'twine' n'est pas installé. Installation en cours..."
    pip install twine
else
    echo "Le paquet 'twine' est déjà installé."
fi

# Lire le fichier de version
VERSION=$(cat "$VERSION_FILE")

# Extraire les numéros de version
MAJOR=$(echo "$VERSION" | jq -r .major)
MINOR=$(echo "$VERSION" | jq -r .minor)
PATCH=$(echo "$VERSION" | jq -r .patch)

git status

# Demander le type de mise à jour
echo "Quel type de mise à jour souhaitez-vous effectuer ?"
echo "1. Mise à jour majeure (major)"
echo "2. Mise à jour mineure (minor)"
echo "3. Mise à jour de correctif (patch)"
read -p "Choisissez 1, 2 ou 3 : " UPDATE_TYPE

case $UPDATE_TYPE in
  1)
    # Mise à jour majeure
    MAJOR=$((MAJOR + 1))
    MINOR=0
    PATCH=0
    ;;
  2)
    # Mise à jour mineure
    MINOR=$((MINOR + 1))
    PATCH=0
    ;;
  3)
    # Mise à jour de correctif
    PATCH=$((PATCH + 1))
    ;;
  *)
    echo "Choix invalide. Le script s'est arrêté."
    exit 1
    ;;
esac

# Mettre à jour le fichier de version
echo "{\"major\":$MAJOR,\"minor\":$MINOR,\"patch\":$PATCH}" > "$VERSION_FILE"

# Afficher la nouvelle version
echo "Nouvelle version : $MAJOR.$MINOR.$PATCH"

# Ajouter les fichier de version modifié à l'index git
git add -A

read -p "Entrez le message de tag : " COMMIT_MESSAGE

git commit -m "$COMMIT_MESSAGE"

git tag "$MAJOR.$MINOR.$PATCH"

git push --tags

git push

rm -rf dist
rm -rf build

python setup.py sdist bdist_wheel

twine check dist/*

twine upload dist/*

echo "Le script s'est terminé avec succès."