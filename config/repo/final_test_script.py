import yaml
import os

def combine_yaml_files(allowed_pushes_path, repo_mapping_path, output_path):
    # Load repo_mapping.yml first (we keep the '---' for the first document)
    with open(repo_mapping_path, 'r') as f:
        repo_mapping = f.read()  # Keep the '---' separator for the first document

    # Load allowed_jfrog_pushes.yml as raw text and remove '---'
    with open(allowed_pushes_path, 'r') as f:
        allowed_pushes_raw = f.read()

    # Remove the '---' document separator if present in the second document
    allowed_pushes_raw = allowed_pushes_raw.replace('---\n', '')

    # Load repo_mapping as a dictionary so we can do the alias replacement
    repo_mapping_dict = yaml.safe_load(repo_mapping)

    # Manually replace the aliases with their corresponding values from repo_mapping
    for alias, actual_value in repo_mapping_dict['repo_mapping'].items():
        allowed_pushes_raw = allowed_pushes_raw.replace(f'*{alias}', str(actual_value))

    # Combine the two documents (repo_mapping and modified allowed_pushes) into one structure
    combined_yaml = f"{repo_mapping}\n---\n{allowed_pushes_raw}"

    # Write the combined YAML to the output file
    with open(output_path, 'w') as f:
        f.write(combined_yaml)

def load_combined_yaml(output_path):
    # Load the combined YAML file
    with open(output_path, 'r') as f:
        combined_data = list(yaml.safe_load_all(f))  # Load multiple documents

    # Extract allowed_jfrog_pushes and repo_mapping
    repo_mapping = combined_data[0].get("repo_mapping", {})
    allowed_pushes = combined_data[1].get("allowed_jfrog_pushes", {})
    
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

# Combine the two YAML files into one document with manual alias resolution
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
