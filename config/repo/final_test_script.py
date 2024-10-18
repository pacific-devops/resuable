import os

def check_access(jfrog_repo_name, github_repo_id, folder, combined_yaml_path):
    # Load the combined YAML
    allowed_pushes, repo_mapping = load_combined_yaml(combined_yaml_path)

    # Debug output to check the loaded values
    print(f"Checking access for JFROG_REPO_NAME: {jfrog_repo_name}")
    print(f"GITHUB_REPO_ID: {github_repo_id}")
    print(f"FOLDER: {folder}")
    print(f"Allowed Pushes: {allowed_pushes}")
    print(f"Repo Mapping: {repo_mapping}")

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

# Example usage (from GitHub Actions environment)
jfrog_repo_name = os.environ.get("JFROG_REPO_NAME")
github_repo_id = os.environ.get("GITHUB_REPO_ID")
folder = os.environ.get("FOLDER")

# Check access using the combined YAML file
if check_access(jfrog_repo_name, github_repo_id, folder, combined_yaml_path):
    print("Access granted")
else:
    print("Access denied")
