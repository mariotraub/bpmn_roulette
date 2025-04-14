#!/bin/bash

# Camunda REST API endpoint
CAMUNDA_URL="http://localhost:8080/engine-rest/process-definition/key/roulette-game/start"

# Generate a random business key using uuidgen
BUSINESS_KEY=$(uuidgen)

# Create JSON payload with int variable and random businessKey
read -r -d '' PAYLOAD << EOM
{
  "variables": {
    "money": {
      "value": 200,
      "type": "Integer"
    }
  },
  "businessKey": "$BUSINESS_KEY"
}
EOM

# Start the process instance using curl
curl -X POST "$CAMUNDA_URL" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD"

# Print confirmation
echo "Started Camunda process with businessKey: $BUSINESS_KEY"

echo "Starting Python Service"
python src/main.py
