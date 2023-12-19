#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

rm -f ./*.pid

printf "[Zampo] Checking PostgreSQL availability...\n"
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -q
do
  printf "[Zampo] Database unavailable, waiting 1 second...\n"
  sleep 1;
done
printf "[Zampo] Database available!\n"

exec "$@"