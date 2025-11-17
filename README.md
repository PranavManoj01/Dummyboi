# Image Processing API

**Project ID:** P67  
**Course:** UE23CS341A  
**Academic Year:** 2025  
**Semester:** 5th Sem  
**Campus:** EC  
**Branch:** CSE  
**Section:** G  
**Team:** ImageNets

## 📋 Project Description

An API that allows users to upload an image and apply various transformations like resizing, cropping, or adding filters.

This repository contains the source code and documentation for the Image Processing API project, developed as part of the UE23CS341A course at PES University.

## 🧑‍💻 Development Team (ImageNets)

- [@PranavManoj01](https://github.com/PranavManoj01) - Scrum Master
- [@Peeyushhhhh](https://github.com/Peeyushhhhh) - Developer Team
- [@Taheer322](https://github.com/Taheer322) - Developer Team
- [@pes2ug23cs400-tech](https://github.com/pes2ug23cs400-tech) - Developer Team

## 👨‍🏫 Teaching Assistant

- [@Omicarr](https://github.com/Omicarr)
- [@PES2UG22CS175](https://github.com/PES2UG22CS175)
- [@PES2UG22CS190](https://github.com/PES2UG22CS190)
- [@Accuracy-exe](https://github.com/Accuracy-exe)

## 👨‍⚖️ Faculty Supervisor

- [@sheela824](https://github.com/sheela824)


## Features Overview

### Analysis Features
- **Image Quality Analysis** - Analyze blur, brightness, contrast, and object count
- **Auto Enhancement** - Automatically improve image quality
- **Batch Processing** - Process up to 10 images simultaneously
- **Smart Ratings** - Quality assessment (Poor/Fair/Good/Excellent)
- **Recommendations** - Get suggestions to improve image quality

### Transformation Features
- **Resize** - Resize by fixed dimensions or percentage
- **Crop** - Extract specific regions from images
- **Filters** - Apply 6 artistic filters (blur, sharpen, edge, smooth, grayscale, sepia)
- **Rotate** - Rotate images by any angle (-360° to 360°)
- **Flip** - Mirror images horizontally or vertically

### DevOps & Quality
- **CI/CD Pipeline** - Automated testing with GitHub Actions
- **45+ Test Cases** - Comprehensive coverage (90%+)
- **Web UI Tester** - Beautiful interface for testing all features
- **CORS Support** - Works with web applications

## Development Guidelines

### Branching Strategy
- `main`: Production-ready code
- `develop`: Development branch
- `APIFEATURE/*`: Feature branches
- `APIINFRA/*`: Infrastructure branches
- `APITRANSFORMATION/*`: Transformation branch\
- `refactor/*`: Refactoring branches
- `testing/*`: Implementing test branch
- `bugfix/*`: Bug fix branches

### Commit Messages
Follow conventional commit format:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Test-related changes

### Code Review Process
1. Create feature branch from `develop`
2. Make changes and commit
3. Create Pull Request to `develop`
4. Request review from team members
5. Merge after approval

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/pestechnology/PESU_EC_CSE_G_P67_Image_Processing_API_ImageNets.git
cd PESU_EC_CSE_G_P67_Image_Processing_API_ImageNets
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Tests
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=. --cov-report=html

# View coverage report
start htmlcov/index.html
```

### 5. Start API Server
```bash
python -m uvicorn main:app --reload
```

Server runs on: **http://localhost:8000**

### 6. Test Using Web UI
- Open `api_tester.html` in your browser
- Upload images and test all features
- Download processed images with one click

## API Endpoints

### Root Endpoint
```
GET /
```
Returns available endpoints and API version.

### Analysis Endpoints

#### Analyze Image
```
POST /analyze
```
Analyze image quality without modification.

**Response:**
```json
{
  "filename": "photo.jpg",
  "analysis": {
    "blur_score": 75.5,
    "brightness": 60.2,
    "contrast": 45.8,
    "object_count": 3,
    "quality_rating": "Good"
  },
  "recommendations": [...]
}
```

#### Enhance Image
```
POST /enhance
```
Auto-enhance image and save result.

**Returns:** Original metrics, enhanced metrics, improvements, download URL

#### Batch Analyze
```
POST /batch-analyze
```
Analyze multiple images (max 10).

### Transformation Endpoints

#### Resize Image
```
POST /resize?width=800&height=600
POST /resize?percentage=50
```

**Query Parameters:**
- Option 1: `width` and `height` (fixed dimensions)
- Option 2: `percentage` (1-500%)

#### Crop Image
```
POST /crop?x=100&y=100&width=500&height=500
```

**Query Parameters:**
- `x` - Starting X coordinate
- `y` - Starting Y coordinate
- `width` - Crop width
- `height` - Crop height

#### Apply Filter
```
POST /filter?filter_type=grayscale
```

**Available Filters:**
- `blur` - Blur effect
- `sharpen` - Enhance details
- `edge` - Edge detection
- `smooth` - Smooth effect
- `grayscale` - Black and white
- `sepia` - Vintage effect

#### Rotate Image
```
POST /rotate?angle=45
```

**Query Parameters:**
- `angle` - Rotation angle (-360 to 360)

#### Flip Image
```
POST /flip?direction=horizontal
```

**Query Parameters:**
- `direction` - `horizontal` or `vertical`

#### Download Processed Image
```
GET /download/{file_id}
```
Download previously processed image.

## Using the Web UI Tester

The `api_tester.html` file provides a beautiful interface for testing all features.

### Features:
- Tab-based navigation (Analysis, Transformations, Batch)
- Real-time processing with loading indicators
- Beautiful gradients and color-coded cards
- Working download buttons for all transformations
- Mobile-responsive design

### How to Use:
1. Open `api_tester.html` in browser
2. Select an image file
3. Choose transformation/analysis
4. View results immediately
5. Click "Download Image" button to save

## Example Usage

### Using cURL

**Analyze an Image:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@myimage.jpg"
```

**Resize to 50%:**
```bash
curl -X POST "http://localhost:8000/resize?percentage=50" \
  -F "file=@myimage.jpg"
```

**Crop Region:**
```bash
curl -X POST "http://localhost:8000/crop?x=100&y=100&width=500&height=500" \
  -F "file=@myimage.jpg"
```

**Apply Grayscale Filter:**
```bash
curl -X POST "http://localhost:8000/filter?filter_type=grayscale" \
  -F "file=@myimage.jpg"
```

**Rotate 45 Degrees:**
```bash
curl -X POST "http://localhost:8000/rotate?angle=45" \
  -F "file=@myimage.jpg"
```

**Flip Horizontally:**
```bash
curl -X POST "http://localhost:8000/flip?direction=horizontal" \
  -F "file=@myimage.jpg"
```

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── .gitignore
├── .pytest_cache/
├── CACHEDIR.TAG
├── README.md
├── htmlcov/
├── main.py
├── pytest.ini
├── requirements.txt
├── .pylintrc
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   └── image_processor.py  
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── analysis.py         
│   │   └── transformations.py  
│   │
│   └── utils/
│      ├── __init__.py
│      └── file_handler.py     
├── tests/
│   ├── conftest.py             
│   │
│   ├── unit/
│   │   ├── test_analyzer.py        
│   │   └── test_transformations.py 
│   │
│   ├── integration/
│   │   ├── test_endpoints.py       
│   │   └── Integration_testing.py  
│   │
│   └── system/
│      ├── test_complete_workflow.py 
│      └── test_edge_cases.py        
├── uploads/
├── api_tester.html
└── v/
```

## Testing

### Run All Tests
```bash
pytest tests/ -v --cov=.
```

### Run Specific Test File
```bash
pytest tests/unit/test_analyzer.py -v
pytest tests/unit/test_transformations.py -v
pytest tests/integration/Integration_testing.py -v
pytest tests/system/test_complete_workflow.py -v
```

### Test Statistics
- **Total Tests:** 60+
- **Code Coverage:** 91%
- **Test Files:** 6
  - `test_analyzer.py` - 15 unit tests
  - `test_transformations.py` - 20+ transformation tests
  - `Integration_testing.py` - 17 chained integration tests
  - `test_endpoints.py` - 8+ endpoint tests
  - `test_complete_workflow.py` - 3 Complete workflow tests
  - `test_edge case.py` - 8 edge case tests

## Technologies Used

| Technology | Purpose |
|-----------|---------|
| FastAPI | Web framework |
| OpenCV | Image processing & transformations |
| Pillow | Image filters & enhancement |
| NumPy | Numerical computations |
| Pytest | Testing framework |
| GitHub Actions | CI/CD automation |

## Technical Details

### Image Quality Metrics

**Blur Detection (Laplacian Variance)**
- Uses Laplacian operator to detect edges
- Higher variance = sharper image
- Range: 0-100

**Brightness (Mean Pixel Value)**
- Calculates average pixel intensity
- Range: 0-100 (0=black, 100=white)

**Contrast (Standard Deviation)**
- Measures spread of pixel values
- Range: 0-100+

**Object Detection (Contour Analysis)**
- Binary thresholding
- Connected component detection
- Counts detected objects

### Quality Rating Algorithm
```
Score = (Blur + Brightness + Contrast) / 3

- Excellent: Score >= 70
- Good: Score >= 50
- Fair: Score >= 30
- Poor: Score < 30
```

## Error Handling

The API gracefully handles:
- Invalid image formats → 400 Bad Request
- Invalid transformation parameters → 400 Bad Request
- Missing files → 404 Not Found
- Batch size exceeded → 400 Bad Request
- Crop area out of bounds → 400 Bad Request
- Invalid filter type → 400 Bad Request

## Performance

### Response Times
- `/analyze` endpoint: 200-500ms
- `/enhance` endpoint: 400-800ms
- `/resize` endpoint: 100-300ms
- `/crop` endpoint: 50-150ms
- `/filter` endpoint: 300-500ms
- `/rotate` endpoint: 200-400ms
- `/flip` endpoint: 50-100ms

### Resource Usage
- Memory: 50-100MB
- Disk (per enhanced image): ~500KB
- CPU: Minimal (async processing)

## CI/CD Pipeline

### GitHub Actions Workflow

The project includes automated testing on every push:

1. **Test Job** - Runs 60+ tests on Python 3.9, 3.10, 3.11
2. **Lint Job** - Code quality checks
3. **Build Job** - Verifies build and creates artifacts

### View Pipeline
- Go to GitHub repository → Actions tab
- See all workflow runs and results
- Check test coverage reports

## Code Coverage Report

```
Total Coverage: 90%+

- main.py: 91%+ (API & transformations)
- test_analyzer.py: 100% (Image analysis)
- test_endpoints.py: 86% (API endpoints)
- test_transformations.py: 95%+ (Transformations)
- test_edge_cases.py: 80% (Boundary conditions)
```

View detailed report: Open `htmlcov/index.html` after running coverage

## Software Engineering Practices

This project demonstrates:
- RESTful API design with FastAPI
- Comprehensive testing (unit, integration, edge case)
- CI/CD automation with GitHub Actions
- Professional code organization
- Proper error handling and validation
- CORS support for web integration
- Documentation and README
- Git version control

## Deployment

### Docker Deployment (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.11

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

Build and run:
```bash
docker build -t image-api .
docker run -p 8000:8000 image-api
```

### Traditional Deployment

```bash
# Production server
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

## Troubleshooting

### API Not Starting
- Check port 8000 is available
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Verify Python 3.9+

### Tests Failing
- Delete `__pycache__` folders: `find . -type d -name __pycache__ -exec rm -r {} +`
- Reinstall dependencies: `pip install --upgrade -r requirements.txt`
- Run: `pytest tests/ -v`

### Download Not Working
- Ensure API is running
- Check browser console for errors
- Verify file is being created in `uploads/` folder

### CORS Issues
- CORS is already enabled for all origins
- If still having issues, check browser console

## Support & Issues

For bugs or feature requests, open an issue on GitHub.

## License

This project is for educational purposes.

## Authors

Created as B-Tech mini project for Software Engineering course.

## Acknowledgments

- OpenCV for image processing
- FastAPI for web framework
- Pillow for image filters
- Pytest for testing framework

## 📚 Documentation

- [API Documentation](docs/api.md)
- [User Guide](docs/user-guide.md)
- [Developer Guide](docs/developer-guide.md)

---

**Status:** Production Ready  
**Version:** 2.0.0  
**Tests:** 60+ Passing  
**Coverage:** 90%+  
**Last Updated:** 2025-11-10

**Course:** UE23CS341A  
**Institution:** PES University  
**Academic Year:** 2025  
**Semester:** 5th Sem
