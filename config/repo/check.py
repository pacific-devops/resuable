import yaml
import sys
import os

# Load environment variables (provided by the workflow)
github_repo_id = os.getenv("GITHUB_REPO_ID")
jfrog_repo = os.getenv("JFROG_REPO")

# Check if both environment variables are provided
if not github_repo_id or not jfrog_repo:
    print("Error: GITHUB_REPO_ID and JFROG_REPO must be provided as environment variables.")
    sys.exit(1)

# Load the YAML file with the repository mapping
try:
    with open('repo-mapping.yml', 'r') as file:
        data = yaml.safe_load(file)
except FileNotFoundError:
    print("Error: repo-mapping.yml file not found.")
    sys.exit(1)

# Extract allowed JFrog pushes
allowed_jfrog_pushes = data.get('allowed_jfrog_pushes', {})

# Check if the JFrog repository exists in the YAML mapping
allowed_repos = allowed_jfrog_pushes.get(jfrog_repo, [])

# Check if the GitHub repository ID is in the allowed list
if github_repo_id in allowed_repos:
    print(f"Repo ID {github_repo_id} is allowed to push to {jfrog_repo}")
    sys.exit(0)
else:
    print(f"Repo ID {github_repo_id} is NOT allowed to push to {jfrog_repo}")
    sys.exit(1)
