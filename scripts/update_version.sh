#!/bin/bash
source venv/bin/activate

sh scripts/test_code.sh

if [ $? -ne 0 ]; then
    echo "Tests failed. Aborting the update process."
    exit 1
fi

echo "Tests passed. Proceeding with the update."

# Update code documentation
echo "Building the documentation..."
mkdocs build

# Définir le chemin du fichier de version
VERSION_FILE="config/version.json"

# Vérifier si le fichier de version existe
if [ ! -f "$VERSION_FILE" ]; then
  echo "Le fichier de version '$VERSION_FILE' n'existe pas. Assurez-vous qu'il existe avant de continuer."
  exit 1
fi

# Vérifier si le paquet 'wheel' est installé
if ! pip show wheel > /dev/null 2&1 ; then
    echo "Installing wheel..."
    pip install wheel
else
    echo "wheel is already installed."
fi

if ! pip show twine > /dev/null 2&1 ; then
    echo "Installing twine..."
    pip install twine
else
    echo "twine is already installed."
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

echo "Creating a new distribution and uploading it to PyPI.."
echo ""
echo "Suppressing the previous distribution files..."
if [ -d "dist" ]; then
  rm -rf dist
fi
if [ -d "build" ]; then
  rm -rf build
fi
echo "Creating the distribution..."
python3 setup.py sdist bdist_wheel

if [ $? -ne 0 ]; then
  echo "An error occurred while creating the distribution. Aborting the update process."
  exit 1
fi
echo "Checking  the distribution..."
if [ ! -d "dist" ]; then
  echo "The distribution directory does not exist. Aborting the update process."
  exit 1
fi
twine check dist/*
if [ $? -ne 0 ]; then
  echo "The distribution is not valid. Aborting the update process."
  exit 1
fi
echo "Uploading the distribution to PyPI..."
twine upload dist/*
if [ $? -ne 0 ]; then
  echo "An error occurred while uploading the distribution to PyPI. Aborting the update process."
  exit 1
else
  echo "The distribution has been successfully uploaded to PyPI."
  echo ""
fi
echo "Le script s'est terminé avec succès."