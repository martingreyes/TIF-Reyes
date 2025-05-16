#!/bin/bash


echo "Using API_URL from environment variable: $API_URL"

# Run envsubst to replace placeholders in environment.ts with actual environment variable values
envsubst < src/environments/environment.ts > src/environments/environment.tmp.ts && \
mv src/environments/environment.tmp.ts src/environments/environment.ts

# Start the Angular application
exec "$@"