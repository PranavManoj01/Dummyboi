import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime
import uuid
from pathlib import Path
# NOTE: Removed dependency on UPLOAD_DIR and cv2/numpy/ImageAnalyzer from here for cleanup
# These are only used internally by core/utils, or should be imported directly.

# --- NEW/FIXED IMPORTS ---
import cv2
import uuid
from src.core.image_processor import ImageAnalyzer
from main import UPLOAD_DIR
# -------------------------
router = APIRouter(
    prefix="",
    tags=["Transformations"]
)

logger = logging.getLogger(__name__)


def generate_recommendations(blur: float, brightness: float, contrast: float) -> list[str]:
    """
    Generate image quality recommendations based on blur, brightness, and contrast metrics.

    Args:
        blur (float): Blurriness score of the image (0-100, higher is sharper).
        brightness (float): Brightness score of the image (0-100, higher is brighter).
        contrast (float): Contrast score of the image (0-100, higher is stronger contrast).

    Returns:
        list[str]: A list of recommendations for improving image quality.
                   Returns ["Image quality is good!"] if no issues detected.
    """
    recommendations = []

    if blur < 40:
        recommendations.append("Image is too blurry. Consider retaking the photo.")
    if brightness < 30:
        recommendations.append("Image is too dark. Increase lighting.")
    elif brightness > 80:
        recommendations.append("Image is too bright. Reduce exposure.")
    if contrast < 20:
        recommendations.append("Low contrast. Enhance details for better clarity.")

    return recommendations if recommendations else ["Image quality is good!"]


@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """Analyze image quality without modification"""
    try:
        content = await file.read()
        logger.info(f"Received file for analysis: {file.filename}")
        
        # --- Integration Fix (Calling Live Logic) ---
        image = ImageAnalyzer.read_image(content) # Use the core read_image function

        # --- Live Metric Calculation (Replacing Placeholders) ---
        blur_score = ImageAnalyzer.calculate_blur_score(image)
        brightness = ImageAnalyzer.calculate_brightness(image)
        contrast = ImageAnalyzer.calculate_contrast(image)
        object_count = ImageAnalyzer.count_objects(image)
        rating = ImageAnalyzer.get_quality_rating(blur_score, brightness, contrast)
        
        # --- Image Info (Replacing Placeholders) ---
        height, width = image.shape[:2]
       
        recommendations = generate_recommendations(blur_score, brightness, contrast)

        return {
            "filename": file.filename,
            "timestamp": datetime.now().isoformat(),
            "image_info": {
                "width": width, 
                "height": height,
                "size_kb": len(content) / 1024
            },
            "analysis": {
                "blur_score": blur_score,
                "brightness": brightness,
                "contrast": contrast,
                "object_count": object_count,
                "quality_rating": rating
            },
            "recommendations": recommendations
        }
    
    except ValueError as e:
        # NOTE: Using raise...from e is better, but this matches original structure
        raise HTTPException(status_code=400, detail=str(e)) 
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail="Image analysis failed")



# Add enhance endpoint
@router.post("/enhance")
async def enhance_image_endpoint(file: UploadFile = File(...)):
    """Enhance image and return analysis"""
    try:
        content = await file.read()
        
        # NOTE: This line requires ImageAnalyzer class and read_image method to be fully coded
        image = ImageAnalyzer.read_image(content) 

        # calculate original metrics
        original_blur = ImageAnalyzer.calculate_blur_score(image)
        original_brightness = ImageAnalyzer.calculate_brightness(image)
        original_contrast = ImageAnalyzer.calculate_contrast(image)
         
        # enhance endpoint
        enhanced_image = ImageAnalyzer.enhance_image(image)
        enhanced_blur = ImageAnalyzer.calculate_blur_score(enhanced_image)
        enhanced_brightness = ImageAnalyzer.calculate_brightness(enhanced_image)
        enhanced_contrast = ImageAnalyzer.calculate_contrast(enhanced_image)

        # save enhanced image
        file_id = str(uuid.uuid4()) # uuid now defined
        output_path = UPLOAD_DIR / f"{file_id}_enhanced.jpg"
        cv2.imwrite(str(output_path), enhanced_image) # cv2 now defined

        # --- This block must be defined inside the 'try' block before the final return ---
        detailed_response = {
            "filename": file.filename,
            "timestamp": datetime.now().isoformat(),
            "original_metrics": {
                "blur_score": original_blur,
                "brightness": original_brightness,
                "contrast": original_contrast
            },
            "enhanced_metrics": {
                "blur_score": enhanced_blur,
                "brightness": enhanced_brightness,
                "contrast": enhanced_contrast
            },
            "improvements": {
                "blur_improvement": round(enhanced_blur - original_blur, 2),
                "brightness_improvement": round(enhanced_brightness - original_brightness, 2),
                "contrast_improvement": round(enhanced_contrast - original_contrast, 2)
            },
            "download_url": f"/download/{file_id}_enhanced.jpg"
        }
# ---------------------------------------------------------------------------------

        return detailed_response

    except Exception as e:
        # NOTE: Use logger.error("Enhancement error: %s", e) for Pylint compliance
        logger.error(f"Enhancement error: {str(e)}") 
        raise HTTPException(status_code=500, detail="Image enhancement failed")




