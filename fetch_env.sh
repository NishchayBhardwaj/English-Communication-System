#!/bin/bash

echo "Fetching .env from GitHub Secrets..."
echo "${ENV_FILE}" > .env
echo ".env file created successfully!"
