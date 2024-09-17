import os
import requests

def upload_to_jfrog():
    # Define necessary variables
    parent_folder = './java'
    jfrog_repo = 'gtest-generic-dev-local'
    
    # Get JFrog credentials from environment variables
    jfrog_url = os.getenv('JFROG_URL')
    jfrog_user = os.getenv('JFROG_USER')
    jfrog_api_key = os.getenv('JFROG_API_KEY')

    # Check if credentials are provided
    if not all([jfrog_url, jfrog_user, jfrog_api_key]):
        print("Error: Missing JFrog connection details in environment variables.")
        return

    # Loop through files in the parent folder and upload using JFrog REST API
    for root, dirs, files in os.walk(parent_folder):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, parent_folder)
            upload_url = f"{jfrog_url}/{jfrog_repo}/{relative_path}"

            try:
                with open(full_path, 'rb') as f:
                    response = requests.put(upload_url, auth=(jfrog_user, jfrog_api_key), data=f)
                
                if response.status_code == 201:
                    print(f"Successfully uploaded: {relative_path}")
                else:
                    print(f"Failed to upload {relative_path}: {response.status_code} {response.text}")
            except Exception as e:
                print(f"Error uploading {relative_path}: {str(e)}")

# Call the function to upload to JFrog
upload_to_jfrog()
