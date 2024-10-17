import yaml
import os

def load_yaml_with_anchors(allowed_pushes_path, repo_mapping_path):
    # Load repo mapping first to establish anchors
    with open(repo_mapping_path, 'r') as f:
        repo_mapping = yaml.safe_load(f)

    # Load allowed_jfrog_pushes with access to the anchors from repo_mapping
    with open(allowed_pushes_path, 'r') as f:
        allowed_pushes = yaml.safe_load(f)

    return allowed_pushes, repo_mapping

def check_access(jfrog_repo_name, github_repo_id, folder):
    # Load YAML files
    allowed_pushes, repo_mapping = load_yaml_with_anchors(
        "config/repo/allowed_jfrog_pushes.yml",
        "config/repo/repo_mapping.yml"
    )

    # Retrieve the mapped ID from repo_mapping
    github_repo_mapped_id = repo_mapping.get(github_repo_id)

    # Check access
    for repo_name, repo_data in allowed_pushes.items():
        if repo_name == jfrog_repo_name:
            for entry in repo_data:
                if entry["id"] == github_repo_mapped_id:
                    if folder in entry["folders"]:
                        return True
    return False

# Example usage (can be used in GitHub Actions environment)
jfrog_repo_name = os.environ.get("JFROG_REPO_NAME")
github_repo_id = os.environ.get("GITHUB_REPO_ID")
folder = os.environ.get("FOLDER")

if check_access(jfrog_repo_name, github_repo_id, folder):
    print("Access granted")
else:
    print("Access denied")
