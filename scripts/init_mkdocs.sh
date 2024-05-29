#!/bin/sh

# Check if the number of arguments is correct
if [ $# -ne 2 ]; then
  echo "Usage: $0 package_name project_name"
  exit 1
fi

# Assign the arguments to variables
package_name=$1
project_name=$2

echo "Building Documentation Resources for $project_name"
#Install mkdocs if not installed
echo "Installing mkdocs and mkdocstrings"
echo ""
if ! pip show mkdocs > /dev/null 2>&1 ; then
  echo "Installing mkdocs..."
  pip install mkdocs
else
  echo "mkdocs is already installed."
fi
echo ""
if ! pip show mkdocstrings > /dev/null 2>&1 ; then
  echo "Installing mkdocstrings..."
  pip install mkdocstrings[python]
else
  echo "mkdocstrings is already installed."
fi
echo ""
echo "Installing mkdocs: done"
echo ""

# Create mkdocs.yml
echo "Creating mkdocs.yml"

# Create the mkdocs.yml file from the template file
cp /mnt/c/users/mangg/template_files/mkdocs.yml mkdocs.yml

# Replace the placeholder with the project name
sed -i "s/project_name/$project_name/g" mkdocs.yml
echo "mkdocs.yml created successfully"
echo ""


# Make docs directory if it does not exist
if [ ! -d "docs" ]; then
  echo "Making docs directory"
  mkdir docs
else
  echo "docs directory already exists"
fi
echo "Making docs directory: done"
echo ""

echo "Creating index.md in docs directory"
if [ -f "docs/index.md" ]; then
  echo "index.md already exists in docs directory"
else
  # Create index.md in docs directory from the template file
  cp /mnt/c/users/mangg/template_files/docs_index.md docs/index.md
  # Replace the placeholder with the project name
  sed -i "s/project_name/$project_name/g" docs/index.md
  # Replace the placeholder with the package name
  sed -i "s/package_name/$package_name/g" docs/index.md
  echo "index.md created successfully in docs directory"
fi
echo ""


# Create the build_docs.sh script from the template file
echo "Creating build_docs.sh script"
if [ -f "scripts/build_docs.sh" ]; then
  echo "build_docs.sh script already exists"
else
  echo "Creating build_docs.sh script"
  cp /mnt/c/users/mangg/template_files/build_docs.sh scripts/build_docs.sh
  echo "build_docs.sh script created successfully"
fi
echo ""



