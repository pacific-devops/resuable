import os
import sys
import yaml


def main():
    """jfrog repo mapping main function"""
    
    def remove_yaml_delimiters(yaml_content):
        """Remove YAML document delimiters (---) from the beginning of the YAML content."""
        return yaml_content.replace('---', '').strip()

    # Load environment variables (provided by the workflow)
    github_repo_id = os.getenv("GITHUB_REPO_ID")
    jfrog_repo = os.getenv("JFROG_REPO")  # JFrog repository name
    jfrog_folder = os.getenv("JFROG_FOLDER")  # JFrog folder path like 'pace/subfolder'

    # Check if all required environment variables are provided
    if not github_repo_id or not jfrog_repo or not jfrog_folder:
        print(
            "Error: GITHUB_REPO_ID, JFROG_REPO, and JFROG_FOLDER must be provided as environment variables."
        )
        sys.exit(1)

    # Read the repo_mapping.yml and allowed_jfrog_pushes.yml files
    with open(
        "config/repo/repo_mapping.yml", "r", encoding="utf-8"
    ) as file:
        repo_mapping_content = file.read()

    with open(
        "config/repo/allowed_jfrog_pushes.yml",
        "r",
        encoding="utf-8",
    ) as file:
        jfrog_pushes_content = file.read()

    # Remove any YAML delimiters (---) before combining
    repo_mapping_content = remove_yaml_delimiters(repo_mapping_content)
    jfrog_pushes_content = remove_yaml_delimiters(jfrog_pushes_content)

    # Combine both files into a single YAML string
    combined_yaml = repo_mapping_content + "\n" + jfrog_pushes_content

    # Parse the combined YAML string
    try:
        combined_data = yaml.safe_load(combined_yaml)
    except yaml.YAMLError as exc:
        print(f"Error parsing combined YAML: {exc}")
        sys.exit(1)

    # Extract allowed JFrog pushes
    allowed_jfrog_pushes = combined_data.get("allowed_jfrog_pushes", {})
    github_repo_id_str = str(github_repo_id)

    # Check if the JFrog repository exists in the YAML mapping
    allowed_repos = allowed_jfrog_pushes.get(jfrog_repo, [])

    # Iterate over the repositories and check if the current repo ID matches
    for repo_entry in allowed_repos:
        repo_id = str(repo_entry["id"])  # Get the 'id' and convert to string
        folders = repo_entry["folders"]  # Get the allowed folders

        # Check if the provided GitHub repository ID matches this repo's ID
        if github_repo_id_str == repo_id:
            # Check if the folder matches any allowed folders (including subfolders)
            if any(jfrog_folder.startswith(folder) for folder in folders):
                print(
                    f"Repo ID {github_repo_id} is allowed to push to {jfrog_repo}/{jfrog_folder}"
                )
                return  # Success, terminate script naturally
            print(
                f"Repo ID {github_repo_id} does NOT have access to the folder {jfrog_repo}/{jfrog_folder}"
            )
            sys.exit(1)

    # If no match is found after the loop
    print(f"Repo ID {github_repo_id} is NOT allowed to push to {jfrog_repo}")
    sys.exit(1)


main()
