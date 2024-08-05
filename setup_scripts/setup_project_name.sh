#!/bin/bash

# Prompt the user for the project name
echo "Enter the project name:"
read project_name

# Set the LANG environment variable to handle different encodings
export LANG=C

# Function to check if a file is binary
is_binary() {
  file "$1" | grep -qE 'charset=binary|application/octet-stream'
}

# Replace occurrences of "project_name" with the user-provided project name in all file contents excluding .sh, binary, .ico files, and .git directory
find . -type f ! -path "./.git/*" ! -name "*.sh" ! -name "*.ico" | while read -r file; do
  if ! is_binary "$file"; then
    sed -i '' "s/project_name/$project_name/g" "$file"
  fi
done

# Rename directories containing "project_name" in a bottom-up manner, excluding .git directory
find . -depth -type d -name "*project_name*" ! -path "./.git/*" | while read -r dir; do
  new_dir=$(echo "$dir" | sed "s/project_name/$project_name/g")
  mkdir -p "$(dirname "$new_dir")"
  mv "$dir" "$new_dir"
done

# Rename files containing "project_name" excluding .sh, .ico files, and .git directory
find . -depth -type f -name "*project_name*" ! -path "./.git/*" ! -name "*.sh" ! -name "*.ico" | while read -r file; do
  if ! is_binary "$file"; then
    new_file=$(echo "$file" | sed "s/project_name/$project_name/g")
    mv "$file" "$new_file"
  fi
done

echo "Replacement complete."
