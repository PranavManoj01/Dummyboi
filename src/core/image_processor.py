import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

class ImageAnalyzer:
    """Handles image analysis and processing operations"""
    
    @staticmethod
    def read_image(file_content: bytes) -> np.ndarray:
        """Convert bytes to OpenCV image"""
        nparr = np.frombuffer(file_content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Invalid image format")
        return img

    @staticmethod
    def calculate_blur_score(image: np.ndarray) -> float:
        """Calculate blur detection score (0-100)"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        blur_score = min(100, (laplacian_var / 500) * 100)
        return round(blur_score, 2)
    
    @staticmethod
    def calculate_brightness(image: np.ndarray) -> float:
        """Calculate average brightness (0-100)"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        return round((brightness / 255) * 100, 2) 

    @staticmethod
    def count_objects(image: np.ndarray) -> int:
        """Detect and count objects in image"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY) #Changed alpha value orginally 255
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return len(contours)
    
    @staticmethod
    def calculate_contrast(image: np.ndarray) -> float:
        """Calculate image contrast (0-100)"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        contrast = np.std(gray)
        return round((contrast / 128) * 100, 2)
    
    @staticmethod
    def enhance_image(image: np.ndarray) -> np.ndarray:
        """Auto-enhance image quality"""
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        enhancer = ImageEnhance.Contrast(pil_image)
        pil_image = enhancer.enhance(1.3)
        
        enhancer = ImageEnhance.Brightness(pil_image)
        pil_image = enhancer.enhance(1.1)
        
        enhancer = ImageEnhance.Sharpness(pil_image)
        pil_image = enhancer.enhance(1.2)
        
        enhanced = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        return enhanced
    

    @staticmethod
    def get_quality_rating(blur: float, brightness: float, contrast: float) -> str:
        """Generate quality rating based on metrics"""
        score = (blur + brightness + contrast) / 3
        if score >= 70: #orignally 70
            return "Excellent"
        elif score >= 50:
            return "Good"
        elif score >= 30:
            return "Fair"
        else:
            return "Poor"
        

# ==================== TRANSFORMATION METHODS ====================
    
    @staticmethod
    def resize_image(image: np.ndarray, width: int, height: int) -> np.ndarray:
        """Resize image to specified dimensions"""
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive")
        resized = cv2.resize(image, (width, height))
        return resized
    
    @staticmethod
    def resize_by_percentage(image: np.ndarray, percentage: int) -> np.ndarray:
        """Resize image by percentage (50 = 50% of original)"""
        if percentage <= 0 or percentage > 500:
            raise ValueError("Percentage must be between 1 and 500")
        height, width = image.shape[:2]
        new_width = int(width * percentage / 100)
        new_height = int(height * percentage / 100)
        resized = cv2.resize(image, (new_width, new_height))
        return resized
    
    @staticmethod
    def crop_image(image: np.ndarray, x: int, y: int, width: int, height: int) -> np.ndarray:
        """Crop image from position (x,y) with specified dimensions"""
        img_height, img_width = image.shape[:2]

        if x < 0 or y < 0 or width <= 0 or height <= 0:
            raise ValueError("Invalid crop parameters")
        if x + width > img_width or y + height > img_height:
            raise ValueError("Crop area exceeds image boundaries") 
        cropped = image[y:y+height, x:x+width]
        return cropped
    

    @staticmethod
    def apply_filter(image: np.ndarray, filter_type: str) -> np.ndarray:
        """Apply various filters to image"""
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        if filter_type == "blur":
            filtered = pil_image.filter(ImageFilter.BLUR)
        elif filter_type == "sharpen":
            filtered = pil_image.filter(ImageFilter.SHARPEN)
        elif filter_type == "edge":
            filtered = pil_image.filter(ImageFilter.FIND_EDGES)
        elif filter_type == "smooth":
            filtered = pil_image.filter(ImageFilter.SMOOTH)
        elif filter_type == "grayscale":
            filtered = pil_image.convert('L').convert('RGB')
        elif filter_type == "sepia":
            filtered = ImageEnhance.Color(pil_image).enhance(0)
            filtered = ImageEnhance.Brightness(filtered).enhance(0.8)
        else:
            raise ValueError(f"Unknown filter: {filter_type}")
        
        result = cv2.cvtColor(np.array(filtered), cv2.COLOR_RGB2BGR)
        return result
    
    @staticmethod
    def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
        """Rotate image by specified angle (degrees)"""
        height, width = image.shape[:2]
        center = (width // 2, height // 2)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, matrix, (width, height))
        return rotated
    
    @staticmethod
    def flip_image(image: np.ndarray, direction: str) -> np.ndarray:
        """Flip image horizontally or vertically"""
        if direction == "horizontal":
            flipped = cv2.flip(image, 1)
        elif direction == "vertical":
            flipped = cv2.flip(image, 0)
        else:
            raise ValueError("Direction must be 'horizontal' or 'vertical'")
        return flipped