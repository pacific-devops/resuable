import os
import requests
import sys

def main():
    """Main function to fetch and process custom properties from a GitHub repository."""
    
    # Fetch environment variables
    github_token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('GITHUB_REPOSITORY')  # GitHub repository to fetch custom properties from
    custom_property_name = os.getenv('INPUT_CUSTOM_PROPERTY')  # The specific custom property the user wants to fetch

    # Ensure required variables are provided
    if not github_token or not repo_name or not custom_property_name:
        print("Missing required environment variables. Aborting.")
        sys.exit(1)

    # GitHub API URL for fetching the repository details
    api_url = f"https://api.github.com/repos/{repo_name}"

    # Set up the request headers for authentication
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    try:
        # Make the API request with a timeout of 10 seconds
        response = requests.get(api_url, headers=headers, timeout=10)

        # Check if the response was successful
        if response.status_code != 200:
            print(f"Failed to fetch repository details: {response.status_code}")
            sys.exit(1)

    except requests.exceptions.Timeout:
        print("The request timed out.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    # Parse the response JSON
    repo_data = response.json()

    # Fetch the specific custom property from the repo's metadata
    custom_property = repo_data.get('custom_properties', {}).get(custom_property_name, None)

    # Handle the case where the custom property doesn't exist
    if not custom_property:
        print(f"No custom property found for '{custom_property_name}'. Aborting.")
        sys.exit(1)

    # Assume the custom property is a semicolon-separated list (e.g., "value1;value2;value3")
    property_values = [value.strip() for value in custom_property.split(";")]
    print(f"Values for custom property '{custom_property_name}': {property_values}")

    # Write the property values to GitHub output for use in subsequent steps
    github_output_path = os.getenv('GITHUB_OUTPUT')
    
    if github_output_path:
        with open(github_output_path, 'a', encoding='utf-8') as output_file:
            output_file.write(f"{custom_property_name}={','.join(property_values)}\n")
    else:
        print("GITHUB_OUTPUT is not set. Cannot write output.")
        sys.exit(1)

main()  # Calling main() without the if __name__ == "__main__" check
