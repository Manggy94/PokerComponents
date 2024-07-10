#!/bin/bash

# Affiche un message pour indiquer le début des tests
echo "Running tests..."

# Dossier de référence pour la couverture
SOURCE_DIRS="pkrcomponents"

# Execute tests
coverage run --source=$SOURCE_DIRS -m unittest discover -s tests -p "*.py"

# Check if tests failed
if [ $? -ne 0 ]; then
    echo "Tests failed."
    exit 1
fi

# Generate coverage report
coverage report > coverage.txt
coverage html

# Extraire le pourcentage total de couverture
total_coverage=$(grep 'TOTAL' coverage.txt | awk '{print $4}' | sed 's/%//')

# Vérifier si la couverture est supérieure ou égale à 90%
if [ $(echo "$total_coverage >= 98" | bc -l) -eq 1 ]  ; then
    echo "Test coverage is sufficient: ${total_coverage}%"
    exit 0
else
    echo "Test coverage is insufficient: ${total_coverage}%"
    # Afficher le rapport de couverture en html
    exit 1
fi
