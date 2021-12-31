#!/usr/bin/bash
# Creates files with the postgres login details.

read -p "Database name: " dbname
read -p "Database user: " dbuser
read -p "Database password: " dbpass

# cd in the current directory
cd $(realpath "$(dirname "$0")")

mkdir -p secrets
cd secrets
echo "${dbname}" >.postgres_db
echo "${dbuser}" >.postgres_user
echo "${dbpass}" >.postgres_pass

chmod 600 .postgres_*
