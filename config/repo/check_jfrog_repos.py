import os
import requests
import sys
import json

# Use the GitHub-provided environment variables
github_token = os.getenv('GITHUB_TOKEN')
repo_name = os.getenv('GITHUB_REPOSITORY')  # Format: owner/repo
destination_repo = os.getenv('INPUT_DESTINATION_REPO')  # User input

# API URL to fetch custom properties from the repository
api_url = f"https://api.github.com/repos/{repo_name}"

# Fetch custom properties using the GitHub API
headers = {
    'Authorization': f'token {github_token}',
    'Accept': 'application/vnd.github.v3+json'
}

response = requests.get(api_url, headers=headers)

if response.status_code != 200:
    print(f"Failed to fetch repository details: {response.status_code}")
    sys.exit(1)

# Parse the repository data from the GitHub API response
repo_data = response.json()

# Retrieve the custom property 'jfrog_repo'
custom_properties = repo_data.get('custom_properties', {}).get('jfrog_repo', None)

if not custom_properties:
    print("No custom properties found for jfrog_repo.")
    sys.exit(1)

# Split the custom properties into a list (assuming semicolon-separated)
allowed_repos = custom_properties.split(';')

print(f"Allowed repositories: {allowed_repos}")

# Check if the destination repository (provided by the user) is in the allowed repositories
if destination_repo in allowed_repos:
    print(f"The repository {destination_repo} is allowed.")
    
    # Set outputs using GITHUB_OUTPUT environment file
    with open(os.getenv('GITHUB_OUTPUT'), 'a') as output_file:
        output_file.write(f"jfrog_repo={destination_repo}\n")
        output_file.write(f"allowed_repos={';'.join(allowed_repos)}\n")
else:
    print(f"The repository {destination_repo} is not allowed. Aborting.")
    sys.exit(1)
