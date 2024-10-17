import yaml
import os

def check_access(jfrog_repo_name, github_repo_id, folder):
    # Load YAML files
    with open("./allowed_jfrog_pushes.yml", "r") as f:
        allowed_pushes = yaml.safe_load(f)
    with open("/config/repo/repo_mapping.yml", "r") as f:
        repo_mapping = yaml.safe_load(f)

    # Expand alias
    github_repo_id = repo_mapping.get(github_repo_id)

    # Check access
    for repo_name, repo_data in allowed_pushes.items():
        if repo_name == jfrog_repo_name:
            for entry in repo_data:
                if entry["id"] == github_repo_id:
                    if folder in entry["folders"]:
                        return True
                    else:
                        return False
    return False

# Example usage (no longer needed in the actual workflow)
jfrog_repo_name = os.environ.get("JFROG_REPO_NAME")
github_repo_id = os.environ.get("GITHUB_REPO_ID")
folder = os.environ.get("FOLDER")

if check_access(jfrog_repo_name, github_repo_id, folder):
    print("Access granted")
else:
    print("Access denied")
