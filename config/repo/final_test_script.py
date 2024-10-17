import yaml
import os

def load_yaml_files(allowed_pushes_path, repo_mapping_path):
    # Load repo_mapping.yml content
    with open(repo_mapping_path, 'r') as f:
        repo_mapping = yaml.safe_load(f)

    # Load allowed_jfrog_pushes.yml content
    with open(allowed_pushes_path, 'r') as f:
        allowed_pushes = yaml.safe_load(f)

    return allowed_pushes, repo_mapping

def resolve_anchors(allowed_pushes, repo_mapping):
    # Replace aliases (anchors) in allowed_pushes with actual values from repo_mapping
    for repo_name, repo_data in allowed_pushes.items():
        for entry in repo_data:
            # Check if 'id' is an alias, replace it with the corresponding value from repo_mapping
            if isinstance(entry['id'], str) and entry['id'].startswith('*'):
                alias = entry['id'][1:]  # Remove '*' to get the alias name
                if alias in repo_mapping:
                    entry['id'] = repo_mapping[alias]  # Replace alias with actual ID

def check_access(jfrog_repo_name, github_repo_id, folder):
    # Load YAML files
    allowed_pushes, repo_mapping = load_yaml_files(
        "config/repo/allowed_jfrog_pushes.yml",
        "config/repo/repo_mapping.yml"
    )

    # Resolve aliases (anchors)
    resolve_anchors(allowed_pushes, repo_mapping)

    # Check access
    for repo_name, repo_data in allowed_pushes.items():
        if repo_name == jfrog_repo_name:
            for entry in repo_data:
                if entry["id"] == github_repo_id:
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
