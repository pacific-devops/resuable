import os
import requests
import sys

# Fetch environment variables
github_token = os.getenv('GITHUB_TOKEN')
repo_name = os.getenv('GITHUB_REPOSITORY')  # The repository from which we fetch custom properties
destination_repo = os.getenv('INPUT_DESTINATION_REPO')  # User input for the target repo (e.g., JFrog repo)
custom_property_name = os.getenv('INPUT_CUSTOM_PROPERTY')  # The specific custom property the user wants to fetch

# GitHub API URL for the repository's custom properties
api_url = f"https://api.github.com/repos/{repo_name}"

# Set the headers for authentication
headers = {
    'Authorization': f'token {github_token}',
    'Accept': 'application/vnd.github.v3+json'
}

# Fetch the repository data using the GitHub API
response = requests.get(api_url, headers=headers)

if response.status_code != 200:
    print(f"Failed to fetch repository details: {response.status_code}")
    sys.exit(1)

# Parse the repository data
repo_data = response.json()

# Fetch the specific custom property the user is asking for
custom_property = repo_data.get('custom_properties', {}).get(custom_property_name, None)

if not custom_property:
    print(f"No custom property found for '{custom_property_name}'. Aborting.")
    sys.exit(1)

# Case 1: If the custom property is 'jfrog_repo_mapping', compare with user input
if custom_property_name == 'jfrog_repo':
    allowed_repos = [repo.strip() for repo in custom_property.split(";")]

    if destination_repo in allowed_repos:
        print(f"The repository {destination_repo} is allowed.")
        
        # Debugging: Check if GITHUB_OUTPUT is available
        github_output_path = os.getenv('GITHUB_OUTPUT')
        print(f"GITHUB_OUTPUT path: {github_output_path}")
        
        if github_output_path:
            with open(github_output_path, 'a') as output_file:
                output_file.write(f"allowed_repo={destination_repo}\n")
        else:
            print("GITHUB_OUTPUT is not set. Cannot write output.")
            sys.exit(1)

    else:
        print(f"The repository {destination_repo} is not allowed. Aborting.")
        sys.exit(1)

# Case 2: For other custom properties, print the property in a list format
else:
    property_values = [value.strip() for value in custom_property.split(";")]
    print(f"Custom Property ({custom_property_name}): {property_values}")

    # Debugging: Check if GITHUB_OUTPUT is available
    github_output_path = os.getenv('GITHUB_OUTPUT')
    print(f"GITHUB_OUTPUT path: {github_output_path}")

    if github_output_path:
        with open(github_output_path, 'a') as output_file:
            output_file.write(f"{custom_property_name}={property_values}\n")
    else:
        print("GITHUB_OUTPUT is not set. Cannot write output.")
        sys.exit(1)
