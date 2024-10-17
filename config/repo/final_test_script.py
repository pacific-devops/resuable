import yaml
import os

def load_yaml_with_anchors(allowed_pushes_path, repo_mapping_path):
    # First, load the repo mapping into a string
    with open(repo_mapping_path, 'r') as f:
        repo_mapping_content = f.read()

    # Then, load the allowed pushes into a string
    with open(allowed_pushes_path, 'r') as f:
        allowed_pushes_content = f.read()

    # Combine the two YAML contents into one
    combined_yaml_content = repo_mapping_content + "\n" + allowed_pushes_content

    # Load the combined YAML
    combined_data = yaml.safe_load(combined_yaml_content)

    return combined_data

def check_access(jfrog_repo_name, github_repo_id, folder):
    # Load YAML files as a single document
    combined_data = load_yaml_with_anchors(
        "config/repo/allowed_jfrog_pushes.yml",
        "config/repo/repo_mapping.yml"
    )

    # Extract repo_mapping and allowed_pushes from the combined document
    repo_mapping = combined_data.get("repo_mapping", {})
    allowed_pushes = combined_data.get("allowed_jfrog_pushes", {})

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
