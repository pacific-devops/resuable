import yaml
import os

# Function to combine two YAML files into one (without nesting the structure)
def combine_yaml_files(allowed_pushes_path, repo_mapping_path, output_path):
    # Load repo_mapping.yml first
    with open(repo_mapping_path, 'r') as f:
        repo_mapping = yaml.safe_load(f)

    # Load allowed_jfrog_pushes.yml as raw text
    with open(allowed_pushes_path, 'r') as f:
        allowed_pushes_raw = f.read()

    # Remove the '---' document separator if present in the second document
    allowed_pushes_raw = allowed_pushes_raw.replace('---\n', '')

    # Replace aliases with their corresponding values from repo_mapping
    for alias, actual_value in repo_mapping['repo_mapping'].items():
        allowed_pushes_raw = allowed_pushes_raw.replace(f'*{alias}', str(actual_value))

    # Parse the modified allowed_jfrog_pushes.yml content
    allowed_pushes = yaml.safe_load(allowed_pushes_raw)

    # Write the final YAML structure to output (without extra nesting)
    with open(output_path, 'w') as f:
        yaml.dump(allowed_pushes, f, default_flow_style=False)

# Function to load the combined YAML file
def load_combined_yaml(output_path):
    with open(output_path, 'r') as f:
        return yaml.safe_load(f)

# Function to check access using the combined YAML
def check_access(jfrog_repo_name, github_repo_id, folder, combined_yaml_path):
    allowed_pushes = load_combined_yaml(combined_yaml_path)

    # Debug output to check loaded values
    print(f"Checking access for JFROG_REPO_NAME: {jfrog_repo_name}")
    print(f"GITHUB_REPO_ID: {github_repo_id}")
    print(f"FOLDER: {folder}")
    print(f"Allowed Pushes: {allowed_pushes}")
    print(f"Available repositories in allowed_jfrog_pushes: {list(allowed_pushes.keys())}")

    # Check if the jfrog_repo_name exists in allowed_jfrog_pushes
    if jfrog_repo_name in allowed_pushes:
        print(f"Repository {jfrog_repo_name} found in allowed_jfrog_pushes.")
        repo_data = allowed_pushes[jfrog_repo_name]

        # Type check: Ensure github_repo_id is an integer for comparison
        try:
            github_repo_id = int(github_repo_id)
            print(f"GITHUB_REPO_ID converted to integer: {github_repo_id}")
        except ValueError:
            print(f"Error: GITHUB_REPO_ID is not a valid integer: {github_repo_id}")
            return False

        # Loop through the repository data and check the ID and folder
        for entry in repo_data:
            print(f"Checking entry: {entry}")
            if entry.get("id") == github_repo_id:
                print(f"ID match found for {github_repo_id}. Checking folders...")
                if folder in entry.get("folders", []):
                    print(f"Folder match found: {folder}")
                    return True
                else:
                    print(f"Folder mismatch: {folder} not found in {entry['folders']}")
            else:
                print(f"ID mismatch: {entry['id']} does not match {github_repo_id}")
    else:
        print(f"Repository {jfrog_repo_name} not found in allowed_jfrog_pushes.")
    
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
