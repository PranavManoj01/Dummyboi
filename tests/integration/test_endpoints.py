import pytest
import sys
from pathlib import Path
from io import BytesIO

# Ensure the app can be imported
sys.path.insert(0, str(Path(__file__).parent.parent))
from fastapi.testclient import TestClient
from main import app

# Initialize client
client = TestClient(app)

class TestAPIEndpoints:
    """Test API endpoints (Integration Tests)"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns API info"""
        response = client.get("/")
        assert response.status_code == 200, "Root endpoint should return 200"
        data = response.json()
        assert "message" in data, "Response should contain message"
    
    def test_health_check_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_analyze_image_success(self, test_image_file):
        """Test /analyze endpoint with a valid image"""
        img_buffer, filename = test_image_file
        img_buffer.seek(0) # Reset buffer to start of file
        
        response = client.post(
            "/analyze",
            files={"file": (filename, img_buffer, "image/jpeg")}
        )
        
        assert response.status_code == 200, "Should return 200 for valid image"
        data = response.json()
        assert "analysis" in data
        assert "blur_score" in data["analysis"]
        assert "recommendations" in data

    def test_enhance_image_success(self, test_image_file):
        """Test /enhance endpoint"""
        img_buffer, filename = test_image_file
        img_buffer.seek(0)
        
        response = client.post(
            "/enhance",
            files={"file": (filename, img_buffer, "image/jpeg")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "original_metrics" in data
        assert "enhanced_metrics" in data
        assert "download_url" in data

    def test_resize_endpoint_success(self, test_image_file):
        """Test /resize endpoint"""
        img_buffer, filename = test_image_file
        img_buffer.seek(0)
        
        response = client.post(
            "/resize?width=50&height=50",
            files={"file": (filename, img_buffer, "image/jpeg")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["new_size"]["width"] == 50
        assert data["new_size"]["height"] == 50

    def test_analyze_invalid_file(self, invalid_file):
        """Test /analyze with invalid file content"""
        img_buffer, filename = invalid_file
        img_buffer.seek(0)
        
        response = client.post(
            "/analyze",
            files={"file": (filename, img_buffer, "image/jpeg")}
        )
        
        assert response.status_code == 400, "Invalid image should return 400"

    def test_download_nonexistent_file(self):
        """Test downloading non-existent file"""
        response = client.get("/download/nonexistent_file.jpg")
        assert response.status_code == 404, "Should return 404 for missing file"
    # Add these new tests inside your TestAPIEndpoints class

    def test_rotate_image_success(self, test_image_file):
        """Test the /rotate endpoint."""
        img_buffer, filename = test_image_file
        img_buffer.seek(0)
        
        response = client.post(
            "/rotate?angle=90",
            files={"file": (filename, img_buffer, "image/jpeg")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["rotation_angle"] == 90
        assert "download_url" in data

    def test_flip_image_success(self, test_image_file):
        """Test the /flip endpoint."""
        img_buffer, filename = test_image_file
        img_buffer.seek(0)
        
        response = client.post(
            "/flip?direction=horizontal",
            files={"file": (filename, img_buffer, "image/jpeg")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["flip_direction"] == "horizontal"
        assert "download_url" in data

    def test_download_file_success(self, test_image_file):
        """Test the /download endpoint after a transformation."""
        img_buffer, filename = test_image_file
        img_buffer.seek(0)
        
        # First, call an endpoint that creates a file
        resize_response = client.post(
            "/resize?width=50&height=50",
            files={"file": (filename, img_buffer, "image/jpeg")}
        )
        
        assert resize_response.status_code == 200
        download_url = resize_response.json()["download_url"] # e.g., /download/file_id.jpg
        
        # Now, test the download URL
        download_response = client.get(download_url)
        
        assert download_response.status_code == 200
        # Check if we received image data
        assert download_response.headers['content-type'] == 'image/jpeg' 
        assert len(download_response.content) > 0
    # ... (add these to tests/test_endpoints.py) ...

    def test_rotate_image_success(self, test_image_file):
        """Test the /rotate endpoint."""
        img_buffer, filename = test_image_file
        img_buffer.seek(0)
        
        response = client.post(
            "/rotate?angle=90",
            files={"file": (filename, img_buffer, "image/jpeg")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["rotation_angle"] == 90
        assert "download_url" in data

    def test_flip_image_success(self, test_image_file):
        """Test the /flip endpoint."""
        img_buffer, filename = test_image_file
        img_buffer.seek(0)
        
        response = client.post(
            "/flip?direction=horizontal",
            files={"file": (filename, img_buffer, "image/jpeg")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["flip_direction"] == "horizontal"
        assert "download_url" in data

    def test_filter_invalid_type(self, test_image_file):
        """Test /filter endpoint with an invalid filter name."""
        img_buffer, filename = test_image_file
        img_buffer.seek(0)
        
        response = client.post(
            "/filter?filter_type=invalid_filter",
            files={"file": (filename, img_buffer, "image/jpeg")}
        )
        
        assert response.status_code == 400 # Validation should fail

    def test_resize_invalid_params_both_or_neither(self, test_image_file):
        """Test /resize validation: must provide (width, height) OR percentage, not both."""
        img_buffer, filename = test_image_file
        img_buffer.seek(0)
        
        # Test case 1: Providing both
        response = client.post(
            "/resize?width=50&height=50&percentage=50",
            files={"file": (filename, img_buffer, "image/jpeg")}
        )
        assert response.status_code == 400

    def test_crop_invalid_area_out_of_bounds(self, test_image_file):
        """Test /crop validation: crop area exceeds image boundaries."""
        img_buffer, filename = test_image_file
        img_buffer.seek(0)
        
        response = client.post(
            "/crop?x=10&y=10&width=2000&height=2000", # Assumes image is smaller than 2000x2000
            files={"file": (filename, img_buffer, "image/jpeg")}
        )
        assert response.status_code == 400

    def test_flip_invalid_direction(self, test_image_file):
        """Test /flip validation: invalid direction."""
        img_buffer, filename = test_image_file
        img_buffer.seek(0)
        
        response = client.post(
            "/flip?direction=diagonal",
            files={"file": (filename, img_buffer, "image/jpeg")}
        )
        assert response.status_code == 400
    
    def test_batch_analyze_success(self, test_image_file):
        """Test /batch-analyze endpoint with multiple valid images."""
        img_buffer1, filename1 = test_image_file
        img_buffer1.seek(0)
        
        # Create a second distinct file object
        img_buffer2 = BytesIO(img_buffer1.getvalue())
        filename2 = "test2.jpg"
        
        response = client.post(
            "/batch-analyze",
            files=[
                ("files", (filename1, img_buffer1, "image/jpeg")),
                ("files", (filename2, img_buffer2, "image/jpeg"))
            ]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_processed"] == 2
        assert data["total_errors"] == 0
        assert len(data["results"]) == 2