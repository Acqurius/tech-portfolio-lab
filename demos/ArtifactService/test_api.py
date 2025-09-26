"""
Simple test script for Artifact Service API
"""

import requests
import json
import os
import tempfile

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code} - {response.json()}")
    return response.status_code == 200

def test_upload():
    """Test file upload"""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("This is a test file content")
        temp_file = f.name
    
    try:
        # Upload file
        with open(temp_file, 'rb') as f:
            files = {'file': f}
            data = {
                'name': 'test-document',
                'is_public': 'true',
                'metadata': '{"description": "Test file"}'
            }
            response = requests.post(f"{BASE_URL}/api/v1/artifacts/upload", files=files, data=data)
        
        print(f"Upload: {response.status_code} - {response.json()}")
        
        if response.status_code == 200:
            artifact_id = response.json()['artifact_id']
            return artifact_id
        return None
        
    finally:
        # Clean up temp file
        os.unlink(temp_file)

def test_download(artifact_id):
    """Test file download"""
    response = requests.get(f"{BASE_URL}/api/v1/artifacts/{artifact_id}/download")
    print(f"Download: {response.status_code}")
    
    if response.status_code == 200:
        print(f"Downloaded content: {response.text[:50]}...")
        return True
    return False

def test_get_info(artifact_id):
    """Test get artifact info"""
    response = requests.get(f"{BASE_URL}/api/v1/artifacts/{artifact_id}")
    print(f"Get info: {response.status_code} - {response.json()}")
    return response.status_code == 200

def test_get_url(artifact_id):
    """Test get presigned URL"""
    response = requests.get(f"{BASE_URL}/api/v1/artifacts/{artifact_id}/url?expires_in=3600")
    print(f"Get URL: {response.status_code} - {response.json()}")
    return response.status_code == 200

def test_list():
    """Test list artifacts"""
    response = requests.get(f"{BASE_URL}/api/v1/artifacts?page=1&page_size=10")
    print(f"List: {response.status_code} - {response.json()}")
    return response.status_code == 200

def test_delete(artifact_id):
    """Test delete artifact"""
    response = requests.delete(f"{BASE_URL}/api/v1/artifacts/{artifact_id}")
    print(f"Delete: {response.status_code} - {response.json()}")
    return response.status_code == 200

def main():
    """Run all tests"""
    print("Testing Artifact Service API...")
    print("=" * 50)
    
    # Test health
    if not test_health():
        print("Health check failed!")
        return
    
    # Test upload
    artifact_id = test_upload()
    if not artifact_id:
        print("Upload failed!")
        return
    
    # Test other operations
    test_get_info(artifact_id)
    test_get_url(artifact_id)
    test_download(artifact_id)
    test_list()
    
    # Test delete
    test_delete(artifact_id)
    
    print("=" * 50)
    print("All tests completed!")

if __name__ == "__main__":
    main()
