import os
import sys
import yaml

# Load environment variables (provided by the workflow)
github_repo_id = os.getenv("GITHUB_REPO_ID")
jfrog_repo = os.getenv("JFROG_REPO")  # JFrog repository name like 'gdap-maven-dev-local'
jfrog_folder = os.getenv("JFROG_FOLDER")  # JFrog folder path like 'pace/subfolder'

# Check if all required environment variables are provided
if not github_repo_id or not jfrog_repo or not jfrog_folder:
    print("Error: GITHUB_REPO_ID, JFROG_REPO, and JFROG_FOLDER must be provided as environment variables.")
    sys.exit(1)

# Load the repository mapping (repo_mapping.yml)
try:
    with open('config/repo/repo_mapping.yml', 'r', encoding='utf-8') as file:
        repo_data = yaml.safe_load(file)
except FileNotFoundError:
    print("Error: repo-mapping.yml file not found.")
    sys.exit(1)

# Load the JFrog mapping (allowed_jfrog_pushes.yml)
try:
    with open('config/repo/allowed_jfrog_pushes.yml', 'r', encoding='utf-8') as file:
        jfrog_data = yaml.safe_load(file)
except FileNotFoundError:
    print("Error: allowed_jfrog_pushes.yml file not found.")
    sys.exit(1)

# Merge the two YAML dictionaries (bringing repo_mapping anchors into jfrog_data's context)
jfrog_data.update(repo_data)

# Extract allowed JFrog pushes
allowed_jfrog_pushes = jfrog_data.get('allowed_jfrog_pushes', {})

# Check if the JFrog repository exists in the YAML mapping
allowed_repos = allowed_jfrog_pushes.get(jfrog_repo, {})

# Ensure both the GitHub repo ID and allowed IDs are strings
github_repo_id_str = str(github_repo_id)

# Iterate over the repositories and check if the current repo ID is in the mapping
for repo_entry in allowed_repos:
    repo_alias = repo_entry['id']  # Get the 'id' for the alias
    folders = repo_entry['folders']  # Get the allowed folders
    
    # Check if GitHub repo ID matches the alias
    if github_repo_id_str == str(jfrog_data[repo_alias]):
        # Check if the folder matches any allowed folders (including subfolders)
        if any(jfrog_folder.startswith(folder) for folder in folders):
            print(f"Repo ID {github_repo_id} is allowed to push to {jfrog_repo}/{jfrog_folder}")
            sys.exit(0)
        else:
            print(f"Repo ID {github_repo_id} does NOT have access to the folder {jfrog_repo}/{jfrog_folder}")
            sys.exit(1)

# If no match is found
print(f"Repo ID {github_repo_id} is NOT allowed to push to {jfrog_repo}")
sys.exit(1)
