# BonoAI FastAPI Backend

High-performance ML-powered API for calculating osteoporotic fracture risk in postmenopausal women.

## Features

- 🚀 **FastAPI** - Modern, fast web framework with automatic API documentation
- 🔒 **Type Safety** - Full Pydantic validation for requests and responses
- 📊 **ML Models** - XGBoost + Cox Proportional Hazards for risk prediction
- 📈 **Explainability** - SHAP waterfall plots for model interpretability
- ✅ **Testing** - Comprehensive test suite with pytest
- 📝 **Documentation** - Auto-generated OpenAPI/Swagger docs
- 🎯 **Performance** - Models loaded once at startup, not per request
- 📊 **Logging** - Structured logging with configurable levels

## Quick Start

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file (see `.env.example`):

```bash
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
```

### Run Development Server

```bash
# Run with auto-reload
uvicorn app.main:app --reload --port 8000

# Or use the main.py directly
python -m app.main
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py -v
```

## API Endpoints

### POST /api/getRisk/

Calculate fracture risk for a patient.

**Request:**
```json
{
  "riskHorizon": 2,
  "patientData": {
    "sex": "female",
    "age": 65,
    "height": 165,
    "weight": 60,
    "tscore_neck": -2.5,
    "tscore_total_hip": -2.0,
    "tscore_ls": -1.5,
    "tbs": 1.2,
    ...
  }
}
```

**Response:**
```json
{
  "message": "Risk score successfully calculated.",
  "risks": {
    "vertebral": 2.15,
    "hip": 1.45,
    "any": 8.23
  }
}
```

### POST /api/getShapPlot/

Generate SHAP waterfall plot for model explainability.

**Request:**
```json
{
  "riskHorizon": 2,
  "patientData": { ... },
  "fxType": "any"
}
```

**Response:**
```json
{
  "message": "SHAP plot successfully created.",
  "shap_plot": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```

### GET /health

Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development"
}
```

## Project Structure

```
backend-fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py     # API route handlers
│   ├── models/
│   │   ├── __init__.py
│   │   └── patient.py       # Pydantic models
│   └── ml/
│       ├── risk_calculator.py
│       ├── models/          # Pre-trained ML models
│       └── plots/           # SHAP visualization
├── tests/
│   ├── __init__.py
│   └── test_api.py          # API tests
├── requirements.txt
├── pytest.ini
├── .env.example
└── README.md
```

## Development

### Code Quality

```bash
# Format code
black app/ tests/

# Lint code
flake8 app/ tests/

# Type checking
mypy app/
```

### Adding New Features

1. Write tests first (TDD approach)
2. Implement feature
3. Ensure all tests pass
4. Update documentation

## Deployment

### Render.com

```yaml
# render.yaml
services:
  - type: web
    name: bonoai-backend
    runtime: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 4"
    envVars:
      - key: ENVIRONMENT
        value: production
      - key: LOG_LEVEL
        value: INFO
```

### Docker

```bash
# Build image
docker build -t bonoai-backend .

# Run container
docker run -p 8000:8000 bonoai-backend
```

## Performance

- **Model Loading**: Models loaded once at startup (not per request)
- **Async Endpoints**: Non-blocking async/await patterns
- **ASGI Server**: Uvicorn with multiple workers for production
- **Type Validation**: Fast Pydantic validation (Rust-powered)

## Monitoring

- Structured logging with timestamps and log levels
- Health check endpoint for load balancers
- Request/response logging for debugging
- Error tracking with stack traces

## License

This project is for research purposes and is not recommended for deployment in everyday clinical settings at this time.

## Contact

For questions or suggestions, contact: lehmannoliver96@gmail.com
