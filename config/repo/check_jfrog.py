import os
import requests
import sys

def main():
    """Main function to fetch and process custom properties."""
    # Fetch environment variables
    github_token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('GITHUB_REPOSITORY')  # The repository from which we fetch custom properties
    custom_property_name = os.getenv('INPUT_CUSTOM_PROPERTY')  # The specific custom property the user wants to fetch

    if not github_token or not repo_name or not custom_property_name:
        print("Missing required environment variables. Aborting.")
        sys.exit(1)

    # GitHub API URL for the repository's custom properties
    api_url = f"https://api.github.com/repos/{repo_name}"

    # Set the headers for authentication
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Fetch the repository data using the GitHub API
    response = requests.get(api_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch repository details: {response.status_code}")
        sys.exit(1)

    # Parse the repository data
    repo_data = response.json()

    # Fetch the specific custom property the user is asking for
    custom_property = repo_data.get('custom_properties', {}).get(custom_property_name, None)

    if not custom_property:
        print(f"No custom property found for '{custom_property_name}'. Aborting.")
        sys.exit(1)

    # Assume the custom property is a semicolon-separated list (e.g., "value1;value2;value3")
    property_values = [value.strip() for value in custom_property.split(";")]
    print(f"Custom property values based on {custom_property_name}: {property_values}")

    # Write the list to GitHub output for use in the workflow
    property_values_str = ",".join(property_values)  # Convert list to comma-separated string
    github_output_path = os.getenv('GITHUB_OUTPUT')

    if github_output_path:
        with open(github_output_path, 'a', encoding='utf-8') as output_file:
            output_file.write(f"{custom_property_name}={property_values_str}\n")
    else:
        print("GITHUB_OUTPUT is not set. Cannot write output.")
        sys.exit(1)

if __name__ == "__main__":
    main()
