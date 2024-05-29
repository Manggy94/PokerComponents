#!/bin/sh

# This script is used to build the documentation for a Python package using MkDocs.
# It takes the package name
# For the each module and sub-module of the selected package (except __init__.py files), it generates a markdown file from a template in the docs directory and adds its path to the mkdocs.yml file.
# Then it builds the documentation using MkDocs.

if [ $# -ne 1 ]; then
  echo "Usage: $0 package_name"
  exit 1
fi

# Assign the argument to a variable
package_name=$1

# Check if the package exists
if [ ! -d "$package_name" ]; then
  echo "The package '$package_name' does not exist. Please make sure the package exists before running this script."
  exit 1
fi

# Check if the docs directory exists
if [ ! -d "docs" ]; then
  echo "The 'docs' directory does not exist. Please make sure the 'docs' directory exists before running this script."
  exit 1
fi

# Check if the mkdocs.yml file exists
if [ ! -f "mkdocs.yml" ]; then
  echo "The 'mkdocs.yml' file does not exist. Please make sure the 'mkdocs.yml' file exists before running this script."
  exit 1
fi

# Check if the template file exists
template_file="/mnt/c/users/mangg/template_files/docs_module.md"
if [ ! -f "$template_file" ]; then
  echo "The template file '$template_file' does not exist. Please make sure the template file exists before running this script."
  exit 1
fi

# Function to create markdown files for each Python module
create_markdown_file() {
  package_name=$1
  module_path=$2
  relative_path=${module_path#"$package_name/"}
  module_name=$(basename "$relative_path" .py)
  md_file="docs/${relative_path%.py}.md"
  # Convert the module path to a Python import path
  module_python_path=$(echo "${module_path%.py}" | sed 's|/|.|g')
  relative_python_path=$(echo "${relative_path%.py}" | sed 's|/|.|g')
  relative_markdown_file_path="${relative_path%.py}.md"
  mkdir -p "docs/$(dirname "$relative_path")"

  # Create a markdown file from the template
  sed "s/{{module_name}}/$module_name/g; s|{{module_python_path}}|$module_python_path|g; s|{{package_name}}|$package_name|g" "$template_file" > "$md_file"

  # Add the markdown file to mkdocs.yml

  sed -i "/  - API Reference:/a\    - $relative_python_path: $relative_markdown_file_path" mkdocs.yml
}

# Find all Python files in the package (excluding __init__.py) and create markdown files for them
find "$package_name" -name "*.py" ! -name "__init__.py" | while read file; do
  create_markdown_file "$package_name" "$file"
done

# Build the documentation using MkDocs
echo "Building the documentation using MkDocs..."
mkdocs build
mkdocs serve

echo "Documentation built successfully."
