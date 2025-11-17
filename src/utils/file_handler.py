import logging
from pathlib import Path
import numpy as np
import cv2

logger = logging.getLogger(__name__)

# --- Absolute Path Definition (Fixes 404 Test Error) ---
# 1. Get the path to this file (file_handler.py)
# 2. Go up two levels (from src/utils/ to the project root)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
# --------------------------------------------------

def setup_upload_directory():
    """Creates the upload directory if it doesn't exist."""
    if not UPLOAD_DIR.exists():
        UPLOAD_DIR.mkdir()
        logger.info(f"Created missing uploads directory at: {UPLOAD_DIR.resolve()}")
    else:
        logger.info(f"Uploads directory already exists: {UPLOAD_DIR.resolve()}")
def read_image(file_content: bytes) -> np.ndarray:
    """
    Converts raw file bytes from an upload into an OpenCV image array (np.ndarray).
    (Moved from image_processor.py)
    """
    nparr = np.frombuffer(file_content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Invalid image format or failed to decode file content.")
    return img
# --- Run Setup on Import ---
# This ensures the "uploads" folder is created when the app starts
setup_upload_directory()