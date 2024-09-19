import requests
import yaml
import os

# Fetch GitHub token and org name from environment variables
TOKEN = os.getenv('GITHUB_TOKEN')
ORG_NAME = os.getenv('GITHUB_ORG_NAME')

# Check if TOKEN and ORG_NAME are provided
if not TOKEN or not ORG_NAME:
    print("Error: Please set the GITHUB_TOKEN and GITHUB_ORG_NAME environment variables.")
    exit(1)

headers = {'Authorization': f'token {TOKEN}'}

# Fetch repos from the GitHub API
response = requests.get(f'https://api.github.com/orgs/{ORG_NAME}/repos', headers=headers)
if response.status_code != 200:
    print(f"Error: Failed to fetch repos. HTTP Status code: {response.status_code}")
    print(response.text)
    exit(1)

repos = response.json()

# Prepare the YAML structure
repo_mapping = {}
for repo in repos:
    repo_name = repo['name']  # Convert name to match YAML key style
    repo_id = repo['id']
    repo_mapping[repo_name] = f"&{repo_name} {repo_id}"

# Output as YAML
yaml_output = yaml.dump({'repo_mapping': repo_mapping}, default_flow_style=False)
print(yaml_output)
