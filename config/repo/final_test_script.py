import yaml
import os

# Function to combine two YAML files into one (with manual alias replacement)
def combine_yaml_files(allowed_pushes_path, repo_mapping_path, output_path):
    # Load repo_mapping.yml first
    with open(repo_mapping_path, 'r') as f:
        repo_mapping = yaml.safe_load(f)  # Load as a single document

    # Load allowed_jfrog_pushes.yml as raw text
    with open(allowed_pushes_path, 'r') as f:
        allowed_pushes_raw = f.read()

    # Remove the '---' document separator if present in the second document
    allowed_pushes_raw = allowed_pushes_raw.replace('---\n', '')

    # Manually replace the aliases with their corresponding values from repo_mapping
    for alias, actual_value in repo_mapping['repo_mapping'].items():
        allowed_pushes_raw = allowed_pushes_raw.replace(f'*{alias}', str(actual_value))

    # Now parse the modified allowed_jfrog_pushes.yml content
    allowed_pushes = yaml.safe_load(allowed_pushes_raw)

    # Flatten the allowed_pushes and repo_mapping into a single document
    combined_yaml = {**allowed_pushes}  # This will flatten allowed_jfrog_pushes structure

    # Write the combined structure to a single YAML file
    with open(output_path, 'w') as f:
        yaml.dump(combined_yaml, f, default_flow_style=False)

# Function to load the combined YAML
def load_combined_yaml(output_path):
    # Load the combined YAML file
    with open(output_path, 'r') as f:
        combined_data = yaml.safe_load(f)  # Load as a single document

    # No nested 'allowed_jfrog_pushes' key, directly return combined_data
    return combined_data

# Function to check access using the combined YAML
def check_access(jfrog_repo_name, github_repo_id, folder, combined_yaml_path):
    # Load the combined YAML
    allowed_pushes = load_combined_yaml(combined_yaml_path)

    # Debug output to check the loaded values
    print(f"Checking access for JFROG_REPO_NAME: {jfrog_repo_name}")
    print(f"GITHUB_REPO_ID: {github_repo_id}")
    print(f"FOLDER: {folder}")
    print(f"Allowed Pushes: {allowed_pushes}")

    # Check access logic using the resolved aliases (anchors)
    for repo_name, repo_data in allowed_pushes.items():
        print(f"Checking repo: {repo_name}")
        if repo_name == jfrog_repo_name:
            for entry in repo_data:
                print(f"Entry ID: {entry['id']}, Expected: {github_repo_id}")
                if entry["id"] == github_repo_id:
                    print(f"Checking folder: {folder} in {entry['folders']}")
                    if folder in entry["folders"]:
                        return True
    return False

# Paths to the YAML files
allowed_pushes_path = "config/repo/allowed_jfrog_pushes.yml"
repo_mapping_path = "config/repo/repo_mapping.yml"
combined_yaml_path = "config/repo/combined.yml"

# Combine the two YAML files into one document
combine_yaml_files(allowed_pushes_path, repo_mapping_path, combined_yaml_path)

# Example usage (from GitHub Actions environment)
jfrog_repo_name = os.environ.get("JFROG_REPO_NAME")
github_repo_id = os.environ.get("GITHUB_REPO_ID")
folder = os.environ.get("FOLDER")

# Check access using the combined YAML file
if check_access(jfrog_repo_name, github_repo_id, folder, combined_yaml_path):
    print("Access granted")
else:
    print("Access denied")
