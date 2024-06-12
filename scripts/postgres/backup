#!/bin/sh -e

echo "Backup process started."

export POSTGRES_USER="${POSTGRES_USER}"

# Save the current date in YYYY-MM-DD format to a variable
current_datetime=$(date +%Y-%m-%d-%H%M%S)

backup_directory="/backups"
backup_filename="${backup_directory}/backup-${current_datetime}.dump.gz"

# Run pg_dump and compress its output, then save to /backups with the current date in the filename
pg_dump -Fc app -U "$POSTGRES_USER" | gzip > "$backup_filename"


echo "Backup has been created and saved to ${backup_filename}"
