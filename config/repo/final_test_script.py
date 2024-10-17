import yaml
import os
import re

def load_yaml_files(allowed_pushes_path, repo_mapping_path):
    # Load repo_mapping.yml content as a dictionary
    with open(repo_mapping_path, 'r') as f:
        repo_mapping = yaml.safe_load(f)

    # Load allowed_jfrog_pushes.yml content as raw text
    with open(allowed_pushes_path, 'r') as f:
        allowed_pushes_raw = f.read()

    return allowed_pushes_raw, repo_mapping

def resolve_anchors(allowed_pushes_raw, repo_mapping):
    # Remove YAML document marker (---) if present
    allowed_pushes_raw = re.sub(r'---\s*\n', '', allowed_pushes_raw)

    # Manually replace each alias from repo_mapping in the raw text
    for alias, actual_value in repo_mapping.items():
        # Replace the alias in the raw YAML content
        alias_pattern = f"*{alias}"
        allowed_pushes_raw = allowed_pushes_raw.replace(alias_pattern, str(actual_value))

    return allowed_pushes_raw  # Returning the replaced raw YAML string

def check_access(jfrog_repo_name, github_repo_id, folder):
    # Load the raw YAML and mappings
    allowed_pushes_raw, repo_mapping = load_yaml_files(
        "config/repo/allowed_jfrog_pushes.yml",
        "config/repo/repo_mapping.yml"
    )

    # Replace all aliases in the raw YAML content before parsing
    replaced_yaml = resolve_anchors(allowed_pushes_raw, repo_mapping)

    # Parse the replaced YAML content
    try:
        allowed_pushes = yaml.safe_load(replaced_yaml)
    except yaml.YAMLError as exc:
        print(f"YAML Error: {exc}")
        raise

    # Now proceed with checking access
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
