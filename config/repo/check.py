import os
import sys
import yaml

def main():
    """jfrog repo mapping main function"""
    # Load environment variables
    github_repo_id = os.getenv("GITHUB_REPO_ID")
    jfrog_repo = os.getenv("JFROG_REPO")
    jfrog_folder = os.getenv("JFROG_FOLDER")

    if not github_repo_id or not jfrog_repo or not jfrog_folder:
        print("Error: GITHUB_REPO_ID, JFROG_REPO, and JFROG_FOLDER must be provided as environment variables.")
        sys.exit(1)

    # Load the YAML files
    with open('config/repo/allowed_jfrog_pushes.yml', 'r', encoding='utf-8') as file:
        allowed_jfrog_pushes = yaml.safe_load(file)

    with open('config/repo/repo_mapping.yml', 'r', encoding='utf-8') as file:
        repo_mapping = yaml.safe_load(file)

    # Access the relevant data
    allowed_pushes = allowed_jfrog_pushes.get('allowed_jfrog_pushes', {})
    github_repo_id_str = str(github_repo_id)

    # Check if the JFrog repository exists in the YAML mapping
    allowed_repos = allowed_pushes.get(jfrog_repo, [])

    # Iterate over the repositories and check if the current repo ID matches
    for repo_entry in allowed_repos:
        repo_id = str(repo_entry['id'])
        folders = repo_entry['folders']

        if github_repo_id_str == repo_id:
            if any(jfrog_folder.startswith(folder) for folder in folders):
                print(f"Repo ID {github_repo_id} is allowed to push to {jfrog_repo}/{jfrog_folder}")
                return
            else:
                print(f"Repo ID {github_repo_id} does NOT have access to the folder {jfrog_repo}/{jfrog_folder}")
                sys.exit(1)

    print(f"Repo ID {github_repo_id} is NOT allowed to push to {jfrog_repo}")
    sys.exit(1)

main()
