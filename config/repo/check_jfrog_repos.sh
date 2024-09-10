#!/bin/bash

# Input arguments
GITHUB_TOKEN=$1
REPO_NAME=$2

# API call to fetch the custom properties (adjust as per your API)
api_url="https://api.github.com/repos/${REPO_NAME}"

# Fetch custom properties from the GitHub repository (custom property: jfrog_repo)
response=$(curl -s -H "Authorization: token ${GITHUB_TOKEN}" "${api_url}")
custom_properties=$(echo "$response" | jq -r '.custom_properties.jfrog_repo')

if [[ -z "$custom_properties" || "$custom_properties" == "null" ]]; then
  echo "No custom properties found for jfrog_repo."
  exit 1
fi

echo "Custom properties found: $custom_properties"

# Split the custom properties into an array (assuming they are separated by semicolons)
allowed_repos=($(echo $custom_properties | tr ";" "\n"))

# Output the allowed repositories for deployment
for repo in "${allowed_repos[@]}"; do
  echo "Allowed to deploy to: $repo"
done

# Return the allowed repositories for use in the workflow
echo "ALLOWED_REPOS=${allowed_repos[*]}" >> $GITHUB_ENV
