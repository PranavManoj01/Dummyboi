import pytest
import sys
from pathlib import Path
from io import BytesIO

# Ensure the app can be imported
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from fastapi.testclient import TestClient
from main import app

# Initialize client
client = TestClient(app)

class TestSystemWorkflow:
    """
    Tests a complete end-to-end user journey, chaining multiple API calls.
    """

    def test_full_user_journey(self, test_image_file):
        """
        Simulates a full user workflow:
        1. POST to /analyze to check the original image.
        2. POST to /resize to create a new, smaller image.
        3. GET the download URL from the resize response.
        4. POST the *downloaded* (resized) image to /filter.
        5. GET the download URL from the filter response.
        """
        
        # --- Step 1: Analyze the original image ---
        img_buffer, filename = test_image_file
        img_buffer.seek(0)
        
        analyze_response = client.post(
            "/analyze",
            files={"file": (filename, img_buffer, "image/jpeg")}
        )
        assert analyze_response.status_code == 200, "Step 1: Analyze failed"
        
        # --- Step 2: Resize the original image ---
        img_buffer.seek(0) # Reset buffer for the next upload
        resize_response = client.post(
            "/resize?width=50&height=50",
            files={"file": (filename, img_buffer, "image/jpeg")}
        )
        assert resize_response.status_code == 200, "Step 2: Resize failed"
        resize_data = resize_response.json()
        assert resize_data["new_size"]["width"] == 50
        
        # --- Step 3: Download the resized image ---
        download_url_resized = resize_data["download_url"]
        download_response_resized = client.get(download_url_resized)
        
        assert download_response_resized.status_code == 200, "Step 3: Download failed"
        resized_image_bytes = download_response_resized.content
        assert len(resized_image_bytes) > 0

        # --- Step 4: Filter the *resized* image ---
        filter_response = client.post(
            "/filter?filter_type=grayscale",
            files={"file": ("resized_image.jpg", resized_image_bytes, "image/jpeg")}
        )
        assert filter_response.status_code == 200, "Step 4: Filter failed"
        filter_data = filter_response.json()
        assert filter_data["filter_applied"] == "grayscale"
        
        # --- Step 5: Download the final filtered image ---
        download_url_filtered = filter_data["download_url"]
        download_response_filtered = client.get(download_url_filtered)
        
        assert download_response_filtered.status_code == 200, "Step 5: Final download failed"
        assert len(download_response_filtered.content) > 0

    def test_filter_analyze_crop_journey(self, test_image_file):
        """
        Simulates a full user workflow in a different order:
        1. POST to /filter to apply 'sepia'
        2. GET the download URL from the filter response
        3. POST the *downloaded* (filtered) image to /analyze
        4. POST the *same* downloaded image to /crop
        """
        
        # --- Step 1: Filter the original image ---
        img_buffer, filename = test_image_file
        img_buffer.seek(0)
        
        filter_response = client.post(
            "/filter?filter_type=sepia",
            files={"file": (filename, img_buffer, "image/jpeg")}
        )
        assert filter_response.status_code == 200, "Step 1: Filter failed"
        filter_data = filter_response.json()
        assert filter_data["filter_applied"] == "sepia"
        
        # --- Step 2: Download the filtered image ---
        download_url_filtered = filter_data["download_url"]
        download_response_filtered = client.get(download_url_filtered)
        
        assert download_response_filtered.status_code == 200, "Step 2: Download failed"
        filtered_image_bytes = download_response_filtered.content
        assert len(filtered_image_bytes) > 0

        # --- Step 3: Analyze the *filtered* image ---
        analyze_response = client.post(
            "/analyze",
            files={"file": ("filtered_image.jpg", filtered_image_bytes, "image/jpeg")}
        )
        assert analyze_response.status_code == 200, "Step 3: Analyze failed"
        analyze_data = analyze_response.json()
        assert "analysis" in analyze_data
        # Sepia images have low contrast, so we can test this
        assert analyze_data["analysis"]["contrast"] < 30 

        # --- Step 4: Crop the *filtered* image ---
        crop_response = client.post(
            "/crop?x=10&y=10&width=20&height=20",
            files={"file": ("filtered_image.jpg", filtered_image_bytes, "image/jpeg")}
        )
        assert crop_response.status_code == 200, "Step 4: Crop failed"
        crop_data = crop_response.json()
        assert crop_data["cropped_size"]["width"] == 20