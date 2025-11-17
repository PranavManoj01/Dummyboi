import logging
from datetime import datetime
import uuid
# Import FastAPI components needed for all endpoints
from fastapi import APIRouter, UploadFile, File, HTTPException, Query 
from fastapi.responses import FileResponse 

# Import the core logic and utilities (currently located in main.py)
from src.utils.file_handler import UPLOAD_DIR
import cv2
from src.core.image_processor import ImageAnalyzer
logger = logging.getLogger(__name__)

# --- CRITICAL FIX: DEFINE THE ROUTER OBJECT ---
router = APIRouter(
    prefix="",
    tags=["Transformations"]
)

@router.post("/resize")
async def resize_image(
    file: UploadFile = File(...),
    width: int = Query(None),
    height: int = Query(None),
    percentage: int = Query(None)
):
    """Resize image - provide either (width, height) or percentage"""
    try:
        if percentage and (width or height):
            raise ValueError("Provide either percentage OR (width, height), not both")
        if not percentage and (not width or not height):
            raise ValueError("Provide either percentage OR both width and height")
        content = await file.read()
        image = ImageAnalyzer.read_image(content)
        if percentage:
            resized = ImageAnalyzer.resize_by_percentage(image, percentage)
            new_width, new_height = resized.shape[1], resized.shape[0]
        else:
            resized = ImageAnalyzer.resize_image(image, width, height)
            new_width, new_height = width, height
        
        file_id = str(uuid.uuid4())
        output_path = UPLOAD_DIR / f"{file_id}_resized.jpg"
        cv2.imwrite(str(output_path), resized)
        
        return {
            "filename": file.filename,
            "timestamp": datetime.now().isoformat(),
            "original_size": {"width": image.shape[1], "height": image.shape[0]},
            "new_size": {"width": new_width, "height": new_height},
            "transformation": "resize",
            "download_url": f"/download/{file_id}_resized.jpg"
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Resize error: {str(e)}")
        raise HTTPException(status_code=500, detail="Image resize failed")
@router.post("/crop")
async def crop_image(
    file: UploadFile = File(...),
    x: int = Query(...),
    y: int = Query(...),
    width: int = Query(...),
    height: int = Query(...)
):
    """Crop image from position (x,y) with specified dimensions"""
    try:
        content = await file.read()
        image = ImageAnalyzer.read_image(content)
        cropped = ImageAnalyzer.crop_image(image, x, y, width, height)
        file_id = str(uuid.uuid4())
        output_path = UPLOAD_DIR / f"{file_id}_cropped.jpg"
        cv2.imwrite(str(output_path), cropped)
        return {
            "filename": file.filename,
            "timestamp": datetime.now().isoformat(),
            "original_size": {"width": image.shape[1], "height": image.shape[0]},
            "crop_region": {"x": x, "y": y, "width": width, "height": height},
            "cropped_size": {"width": cropped.shape[1], "height": cropped.shape[0]},
            "transformation": "crop",
            "download_url": f"/download/{file_id}_cropped.jpg"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Crop error: {str(e)}")
        raise HTTPException(status_code=500, detail="Image crop failed")
@router.post("/filter")
async def apply_filter(
    file: UploadFile = File(...),
    filter_type: str = Query(...)
):
    """Apply filter to image: blur, sharpen, edge, smooth, grayscale, sepia"""
    try:
        valid_filters = ["blur", "sharpen", "edge", "smooth", "grayscale", "sepia"]
        if filter_type not in valid_filters:
            raise ValueError(f"Filter must be one of: {', '.join(valid_filters)}")
        content = await file.read()
        image = ImageAnalyzer.read_image(content)
        filtered = ImageAnalyzer.apply_filter(image, filter_type)
        file_id = str(uuid.uuid4())
        output_path = UPLOAD_DIR / f"{file_id}_{filter_type}.jpg"
        cv2.imwrite(str(output_path), filtered)
        return {
            "filename": file.filename,
            "timestamp": datetime.now().isoformat(),
            "filter_applied": filter_type,
            "available_filters": ["blur", "sharpen", "edge", "smooth", "grayscale", "sepia"],
            "transformation": "filter",
            "download_url": f"/download/{file_id}_{filter_type}.jpg"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Filter error: {str(e)}")
        raise HTTPException(status_code=500, detail="Filter application failed")
@router.post("/rotate")
async def rotate_image(
    file: UploadFile = File(...),
    angle: float = Query(...)
):
    """Rotate image by specified angle (degrees)"""
    try:
        if angle < -360 or angle > 360:
            raise ValueError("Angle must be between -360 and 360")
        content = await file.read()
        image = ImageAnalyzer.read_image(content)
        rotated = ImageAnalyzer.rotate_image(image, angle)
        file_id = str(uuid.uuid4())
        output_path = UPLOAD_DIR / f"{file_id}_rotated.jpg"
        cv2.imwrite(str(output_path), rotated)
        return {
            "filename": file.filename,
            "timestamp": datetime.now().isoformat(),
            "rotation_angle": angle,
            "transformation": "rotate",
            "download_url": f"/download/{file_id}_rotated.jpg"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Rotate error: {str(e)}")
        raise HTTPException(status_code=500, detail="Image rotation failed")
@router.post("/flip")
async def flip_image(
    file: UploadFile = File(...),
    direction: str = Query(...)
):
    """Flip image horizontally or vertically"""
    try:
        if direction not in ["horizontal", "vertical"]:
            raise ValueError("Direction must be 'horizontal' or 'vertical'")
        content = await file.read()
        image = ImageAnalyzer.read_image(content)
        flipped = ImageAnalyzer.flip_image(image, direction)
        file_id = str(uuid.uuid4())
        output_path = UPLOAD_DIR / f"{file_id}_flipped_{direction}.jpg"
        cv2.imwrite(str(output_path), flipped)
        return {
            "filename": file.filename,
            "timestamp": datetime.now().isoformat(),
            "flip_direction": direction,
            "transformation": "flip",
            "download_url": f"/download/{file_id}_flipped_{direction}.jpg"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Flip error: {str(e)}")
        raise HTTPException(status_code=500, detail="Image flip failed")
@router.get("/download/{file_id}")
async def download_file(file_id: str):
    """Download processed image"""
    file_path = UPLOAD_DIR / file_id
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)



    
