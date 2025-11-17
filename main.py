import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from src.routers import analysis
from src.routers import transformations # <-- NEW: Router for all transforms
# Removed all imports for cv2, numpy, PIL, etc.

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------- FastAPI App ----------------
app = FastAPI(
    title="Smart Image Processing API",
    description="Analyze, enhance, and transform images with quality metrics",
    version="2.0.0"
)

# ---------------- Middleware ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Routers ----------------
app.include_router(analysis.router)
app.include_router(transformations.router) # <-- Task 4: Connect the transformation router

# ---------------- Endpoints ----------------
@app.get("/")
def root():
    """Root endpoint to verify API is running."""
    return {"status": "OK", "message": "Smart Image Processing API is live!"}

@app.get("/health")
def health_check():
    """Health check endpoint for CI/CD monitoring."""
    logger.info("Health check requested")
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    # NOTE: Port 8000 is the default used in the original project setup
    uvicorn.run(app, host="0.0.0.0", port=8000)