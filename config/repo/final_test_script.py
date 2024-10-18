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

    # Replace aliases with their corresponding values from repo_mapping
    for alias, actual_value in repo_mapping['repo_mapping'].items():
        allowed_pushes_raw = allowed_pushes_raw.replace(f'*{alias}', str(actual_value))

    # Parse the modified allowed_jfrog_pushes.yml content
    allowed_pushes_data = yaml.safe_load(allowed_pushes_raw)

    # Since allowed_jfrog_pushes was nested in the file, we extract it directly without wrapping it again
    allowed_pushes = allowed_pushes_data['allowed_jfrog_pushes']

    # Write the allowed_jfrog_pushes content directly into the final YAML file without nesting
    with open(output_path, 'w') as f:
        yaml.dump(allowed_pushes, f, default_flow_style=False)

# Function to load the combined YAML
def load_combined_yaml(output_path):
    # Load the combined YAML file
    with open(output_path, 'r') as f:
        return yaml.safe_load(f)

# Function to check access using the combined YAML
def check_access(jfrog_repo_name, github_repo_id, folder, combined_yaml_path):
    allowed_pushes = load_combined_yaml(combined_yaml_path)

    # Check if the jfrog_repo_name exists in allowed_pushes
    if jfrog_repo_name in allowed_pushes:
        repo_data = allowed_pushes[jfrog_repo_name]

        # Type check: Ensure github_repo_id is an integer for comparison
        try:
            github_repo_id = int(github_repo_id)
        except ValueError:
            print("Error: GITHUB_REPO_ID is not a valid integer.")
            return

        # Loop through the repository data and check the ID and folder
        for entry in repo_data:
            if entry.get("id") == github_repo_id:
                if folder in entry.get("folders", []):
                    print(f"GitHub repo has access to the '{jfrog_repo_name}' and folder '{folder}'.")
                    return
                else:
                    print(f"GitHub repo has access to the '{jfrog_repo_name}' but not the folder '{folder}'.")
                    return
        # If we reach here, GitHub repo has no access
        print(f"GitHub repo does not have access to the '{jfrog_repo_name}'.")
    else:
        print(f"JFrog repository '{jfrog_repo_name}' does not exist.")

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
check_access(jfrog_repo_name, github_repo_id, folder, combined_yaml_path)
