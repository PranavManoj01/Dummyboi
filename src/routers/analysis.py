import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime



logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="",
    tags=["Analysis"]
)


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
        logger.debug(f"File size: {len(content)/1024:.2f} KB")
        
        # NOTE: Replace the placeholders below with the actual calls to src.core/src.utils
        # image = read_image(content) # Use the utility layer function
        image = None # Placeholder for OpenCV image array

        # --- Commit 4 Logic: Metric Placeholders (Refactored) ---
        metrics = {
            "blur_score": 70.0,
            "brightness": 55.0,
            "contrast": 40.0,
            "object_count": 3,
            "quality_rating": "Good"
        } 

        blur_score = metrics["blur_score"]
        brightness = metrics["brightness"]
        contrast = metrics["contrast"]
        object_count = metrics["object_count"]
        rating = metrics["quality_rating"]
        
       
        recommendations = generate_recommendations(blur_score, brightness, contrast)

        return {
            "filename": file.filename,
            "timestamp": datetime.now().isoformat(),
            "image_info": {
                "width": 100, 
                "height": 100,
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
        file_id = str(uuid.uuid4())
        output_path = UPLOAD_DIR / f"{file_id}_enhanced.jpg"
        cv2.imwrite(str(output_path), enhanced_image)

        # original simple return
        simple_response = {"message": "Enhance endpoint created", "filename": file.filename}

        # detailed return added
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

        # return both (you can choose which one to use)
        return detailed_response

    except Exception as e:
        logger.error(f"Enhancement error: {str(e)}")
        raise HTTPException(status_code=500, detail="Image enhancement failed")





