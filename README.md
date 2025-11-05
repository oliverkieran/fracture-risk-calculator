# Bono AI

## Introduction

This is the source code of Bono AI, a machine learning project that aims to compute 2-year fracture risk for postmenopausal women. It includes a website, that lets users compute fracture risks by inputing the required risk factors, and provides further insights into the risk score calculations by displaying SHAP plots. The website will soon be available at [bonoai.ch](https://bonoai.ch).

## Installation

### Frontend

- Navigate to the `frontend` folder with `cd src/frontend`
- Install the dependencies with `npm install`
- Start the development server with `npm run dev`

### Backend

- Navigate to the `backend` folder with `cd src/backend`
- Create a virtual environment: `python -m venv venv`
- Activate the virtual environment:
  - On Linux/Mac: `source venv/bin/activate`
  - On Windows: `venv\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`
- Start the development server: `uvicorn app.main:app --reload --port 8000`
- Visit the interactive API documentation at http://localhost:8000/docs

> [!TIP]
> The backend is now a stateless API and doesn't require a database. Configuration is managed via environment variables (see `.env.example`).

## Architecture

### Frontend

The frontend is built with [React](https://react.dev/), TypeScript and [shadcn/ui](https://ui.shadcn.com/). Requests to the backend are made with [Axios](https://axios-http.com/).

### Backend

The backend is built with [FastAPI](https://fastapi.tiangolo.com/), a modern, high-performance Python web framework. The API is stateless and serves ML model predictions via two main endpoints:

- `POST /api/getRisk/` - Calculate fracture risk scores
- `POST /api/getShapPlot/` - Generate SHAP explainability plots

Key features:
- **Auto-generated documentation**: Interactive API docs at `/docs` (Swagger UI)
- **Type safety**: Full Pydantic validation for all inputs
- **High performance**: ASGI server with async support
- **Comprehensive testing**: 19 tests covering all endpoints and validation

#### ML Dependencies

- pandas
- numpy
- xgboost
- scikit-survival
- shap
- matplotlib

#### API Framework

- fastapi
- uvicorn
- pydantic
- pydantic-settings

### Deployment

The frontend and the backend are deployed separately. Both are deployed on [Render](https://render.com/).

**Backend deployment** (FastAPI):
- Build command: `./build.sh`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 4`
- Health check: `/health`
- See `src/backend/render.yaml` for configuration

**Frontend deployment** (Vite/React):
- Build command: `npm run build`
- Static site serving

## Testing

### Backend Tests

The backend includes a comprehensive test suite:

```bash
cd src/backend
pytest tests/ -v
```

**19 tests covering**:
- Risk calculation for all fracture types
- Input validation for all 48+ patient fields
- SHAP plot generation
- Health checks and API documentation

### Frontend Testing

```bash
cd src/frontend
npm test
```

## Project Structure

```
fracture-risk-calculator/
├── src/
│   ├── backend/           # FastAPI backend
│   │   ├── app/
│   │   │   ├── main.py           # FastAPI app
│   │   │   ├── api/              # Endpoints
│   │   │   ├── models/           # Pydantic models
│   │   │   └── ml/               # ML risk calculator
│   │   ├── tests/                # Backend tests
│   │   ├── requirements.txt
│   │   └── README.md
│   └── frontend/          # React frontend
│       ├── src/
│       │   ├── components/       # React components
│       │   ├── context/          # Context providers
│       │   └── types/            # TypeScript types
│       ├── package.json
│       └── README.md
├── README.md              # This file
└── render.yaml            # Deployment configuration
```

## Notes

- This project is for research purposes and is not recommended for deployment in everyday clinical settings at this time.
- The backend has been migrated from Django to FastAPI for improved performance and developer experience.

## Contact

If you have any questions or suggestions, feel free to contact me at [lehmannoliver96@gmail.com](mailto:lehmannoliver96@gmail.com)
