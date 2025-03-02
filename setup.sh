#!/bin/bash

# Function to check if a file is binary
is_binary() {
  file "$1" | grep -qE 'charset=binary|application/octet-stream'
}

# Make sure nothing is running on port 5432
echo "Making sure nothing is running on port 5432..."
sudo lsof -i :5432 | grep LISTEN | awk '{print $2}' | sudo xargs kill
clear

# Make the user start Docker
read -p "Please start Docker before proceeding. Confirm docker is started by writing 'ACK': " docker_started
if [[ "$docker_started" != "ACK" && "$docker_started" != "ack" ]]; then
  echo "Docker not started. Exiting..."
  exit 1
fi
clear

# Prompt the user for the support email
read -p "Enter the support email: " support_email

# Prompt the user for the project title on the same line
read -p "Enter the project title: " project_title
clear

echo "Replacing placeholders with user-provided values..."

# Convert project title to a lowercased, underscore-separated version
project_name=$(echo "$project_title" | tr '[:upper:]' '[:lower:]' | tr ' ' '_')
project_name_caps=$(echo "$project_title" | tr '[:lower:]' '[:upper:]' | tr ' ' '_')

if [[ "$project_name" =~ [\'\"] ]]; then
  echo "Error: Project name contains apostrophes or quotes."
  exit 1
fi

# Set the LANG environment variable to handle different encodings
export LANG=C

# Replace occurrences of "project_support_email" with the user-provided support email in all file contents excluding binary, .ico files, and .git directory
find . -type f ! -path "./.git/*" ! -name "*.ico" | while read -r file; do
  if ! is_binary "$file"; then
    sed -i '' "s/project_support_email/$support_email/g" "$file"
  fi
done

# Replace occurrences of "project_name" and "project-name" with the user-provided project name in all file contents excluding binary, .ico files, and .git directory, but including bash scripts not named setup.sh
find . -type f ! -path "./.git/*" ! -name "*.ico" ! -name "setup.sh" | while read -r file; do
  if ! is_binary "$file"; then
    sed -i '' "s/project_name/$project_name/g; s/project-name/$project_name/g" "$file"
  fi
done

# Replace occurrences of "project_name_caps" with the user-provided project name in all file contents excluding binary, .ico files, and .git directory
find . -type f ! -path "./.git/*" ! -name "*.ico" | while read -r file; do
  if ! is_binary "$file"; then
    sed -i '' "s/project_name_caps/$project_name_caps/g" "$file"
  fi
done

# Replace occurrences of "project_title" with the user-provided project title in all file contents excluding binary, .ico files, and .git directory
find . -type f ! -path "./.git/*" ! -name "*.ico" | while read -r file; do
  if ! is_binary "$file"; then
    sed -i '' "s/project_title/$project_title/g" "$file"
  fi
done

# Rename directories containing "project_name" or "project-name" in a bottom-up manner, excluding .git directory
find . -depth -type d \( -name "*project_name*" -o -name "*project-name*" \) ! -path "./.git/*" | while read -r dir; do
  new_dir=$(echo "$dir" | sed "s/project_name/$project_name/g; s/project-name/$project_name/g")
  mkdir -p "$(dirname "$new_dir")"
  mv "$dir" "$new_dir"
done

# Rename files containing "project_name" or "project-name" excluding .sh and .ico files, and .git directory
find . -depth -type f \( -name "*project_name*" -o -name "*project-name*" \) ! -path "./.git/*" ! -name "*.sh" ! -name "*.ico" | while read -r file; do
  if ! is_binary "$file"; then
    new_file=$(echo "$file" | sed "s/project_name/$project_name/g; s/project-name/$project_name/g")
    mv "$file" "$new_file"
  fi
done
clear

# Pull a Postgres Docker image
echo "Pulling a Postgres Docker image..."
docker pull postgres
clear

# Create a container named "project_name_db" with the Postgres image
echo "Creating a container named '${project_name}_db' with the Postgres image..."
# Delete the container if it already exists
docker rm -f "${project_name}_db"
docker run --name "${project_name}_db" -e POSTGRES_PASSWORD=postgres -e "POSTGRES_DB=${projectname}_db" -d -p 5432:5432 postgres
clear

# Initialize a virtual environment and install dependencies for the backend
echo "Initializing a virtual environment and installing dependencies for the backend..."
backend_dir="./backend/$project_name"
if [ -d "$backend_dir" ]; then
  cd "$backend_dir" || exit
  python3 -m venv .venv
  source .venv/bin/activate
  if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
  fi
  if [ -f "dev_requirements.txt" ]; then
    pip install -r dev_requirements.txt
  fi
  echo "Virtual environment setup and dependencies installed in $backend_dir/.venv"
  # Initiate Alembic
  deactivate
  cd ..
  mkdir -p alembic/versions
  alembic init alembic
  alembic revision --autogenerate -m "Initial migration"
  alembic upgrade head
else
  echo "Backend directory $backend_dir not found."
fi
clear


# Install Node.js dependencies for the web directory
echo "Installing Node.js dependencies for the web directory..."
cd .. || exit
web_dir="./web"
if [ -d "$web_dir" ]; then
  cd "$web_dir" || exit
  if [ -f "package.json" ]; then
    npm install
    echo "Node.js dependencies installed and package-lock.json created in $web_dir"
  else
    echo "package.json not found in $web_dir"
  fi
else
  echo "Web directory $web_dir not found."
fi
clear


# Remove the .git folder and reinitialize it
echo "Creating a new git repository..."
rm -rf .git
git init
git add -A
git commit -m "Initial commit"
clear
