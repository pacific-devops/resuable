import yaml
import os

def load_yaml_files(allowed_pushes_path, repo_mapping_path):
    # Load repo_mapping.yml content as dictionary
    with open(repo_mapping_path, 'r') as f:
        repo_mapping = yaml.safe_load(f)

    # Load allowed_jfrog_pushes.yml content as raw text
    with open(allowed_pushes_path, 'r') as f:
        allowed_pushes_raw = f.read()

    return allowed_pushes_raw, repo_mapping

def resolve_anchors(allowed_pushes_raw, repo_mapping):
    # Replace aliases manually before loading YAML
    for alias, actual_value in repo_mapping.items():
        # Replace *alias with actual value in the raw YAML content
        allowed_pushes_raw = allowed_pushes_raw.replace(f'*{alias}', str(actual_value))

    # Now parse the modified YAML content after replacements
    allowed_pushes = yaml.safe_load(allowed_pushes_raw)
    return allowed_pushes

def check_access(jfrog_repo_name, github_repo_id, folder):
    # Load YAML files
    allowed_pushes_raw, repo_mapping = load_yaml_files(
        "config/repo/allowed_jfrog_pushes.yml",
        "config/repo/repo_mapping.yml"
    )

    # Resolve anchors (manual alias resolution)
    allowed_pushes = resolve_anchors(allowed_pushes_raw, repo_mapping)

    # Check access logic after alias resolution
    for repo_name, repo_data in allowed_pushes.items():
        if repo_name == jfrog_repo_name:
            for entry in repo_data:
                if entry["id"] == github_repo_id:
                    if folder in entry["folders"]:
                        return True
    return False

# Example usage in a GitHub Actions environment
jfrog_repo_name = os.environ.get("JFROG_REPO_NAME")
github_repo_id = os.environ.get("GITHUB_REPO_ID")
folder = os.environ.get("FOLDER")

if check_access(jfrog_repo_name, github_repo_id, folder):
    print("Access granted")
else:
    print("Access denied")
