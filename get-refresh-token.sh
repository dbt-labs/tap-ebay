#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 client_id redirect_uri client_secret code"
    exit 1
fi

# configured in eBay Developer Dashboard

client_id=$1
redirect_uri=$2
client_secret=$3
code=$4

curl https://api.ebay.com/identity/v1/oauth2/token \
  --header "Content-Type: application/x-www-form-urlencoded" \
  --header "Authorization: Basic $( echo -n "$client_id:$client_secret" | base64  )" \
  --data "grant_type=authorization_code&code=$code&redirect_uri=$redirect_uri"
