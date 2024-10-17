import yaml
import os

def combine_yaml_files(allowed_pushes_path, repo_mapping_path, output_path):
    # Load the allowed_jfrog_pushes.yml content as raw text
    with open(allowed_pushes_path, 'r') as f:
        allowed_pushes_raw = f.read()

    # Load the repo_mapping.yml content as raw text
    with open(repo_mapping_path, 'r') as f:
        repo_mapping_raw = f.read()

    # Combine the two YAML documents into one string with document separator (---)
    combined_yaml_raw = f"{allowed_pushes_raw}\n---\n{repo_mapping_raw}"

    # Write the combined YAML to a new file
    with open(output_path, 'w') as f:
        f.write(combined_yaml_raw)

def load_combined_yaml(output_path):
    # Load the combined YAML file, allowing it to handle anchors and aliases
    with open(output_path, 'r') as f:
        documents = list(yaml.safe_load_all(f))  # Load all documents in the YAML file

    # Extract documents from the loaded YAML
    allowed_pushes = documents[0].get("allowed_jfrog_pushes", {})
    repo_mapping = documents[1].get("repo_mapping", {})
    
    return allowed_pushes, repo_mapping

def check_access(jfrog_repo_name, github_repo_id, folder, combined_yaml_path):
    # Load the combined YAML
    allowed_pushes, repo_mapping = load_combined_yaml(combined_yaml_path)

    # Check access logic using the resolved aliases (anchors)
    for repo_name, repo_data in allowed_pushes.items():
        if repo_name == jfrog_repo_name:
            for entry in repo_data:
                if entry["id"] == github_repo_id:
                    if folder in entry["folders"]:
                        return True
    return False

# Paths to the YAML files
allowed_pushes_path = "config/repo/allowed_jfrog_pushes.yml"
repo_mapping_path = "config/repo/repo_mapping.yml"
combined_yaml_path = "config/repo/combined.yml"

# Combine the two YAML files into one
combine_yaml_files(allowed_pushes_path, repo_mapping_path, combined_yaml_path)

# Example usage (can be used in GitHub Actions environment)
jfrog_repo_name = os.environ.get("JFROG_REPO_NAME")
github_repo_id = os.environ.get("GITHUB_REPO_ID")
folder = os.environ.get("FOLDER")

# Check access using the combined YAML file
if check_access(jfrog_repo_name, github_repo_id, folder, combined_yaml_path):
    print("Access granted")
else:
    print("Access denied")
