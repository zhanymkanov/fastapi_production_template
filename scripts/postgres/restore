#!/bin/sh -e

# The directory where backups are stored
BACKUP_DIRECTORY="/backups"

# Check if a file name was provided as a parameter
if [ $# -eq 0 ]; then
  echo "No file name provided. Please provide a file name to check."
  exit 1
fi

# The file name is taken from the first argument provided to the script
file_name="$1"

# Full path to the file
full_file_path="${BACKUP_DIRECTORY}/${file_name}"

# Check if the file exists
if [ -f "$full_file_path" ]; then
  echo "File ${file_name} exists."
else
  echo "File ${file_name} does not exist."
  exit 1
fi

export POSTGRES_USER="${POSTGRES_USER}"
export POSTGRES_DB="${POSTGRES_DB}"

echo "Dropping the database..."
dropdb "$POSTGRES_DB" -U "$POSTGRES_USER"

echo "Creating a new database..."
createdb "$POSTGRES_DB" --owner="$POSTGRES_USER" -U "$POSTGRES_USER"

echo "Applying the backup to the new database..."
gunzip -c "${full_file_path}" | pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB"

echo "Backup applied successfully."
