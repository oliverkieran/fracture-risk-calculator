# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bono AI is a machine learning application that computes 2-year fracture risk for postmenopausal women. The system uses XGBoost and Cox proportional hazards models to predict three types of fracture risks: vertebral, hip, and any fracture. It provides interpretable predictions using SHAP (SHapley Additive exPlanations) waterfall plots.

## Development Commands

### Frontend (React + TypeScript + Vite)
Navigate to `src/frontend` before running these commands:
- **Install dependencies**: `npm install`
- **Start dev server**: `npm run dev` (runs on http://localhost:5173)
- **Build for production**: `npm run build`
- **Lint code**: `npm run lint`
- **Preview production build**: `npm run preview`

### Backend (Django)
Navigate to `src/backend` before running these commands:
- **Install dependencies**: Create a virtual environment, then install from `requirements.txt`
- **Start dev server**: `python manage.py runserver` (runs on http://localhost:8000)

## Architecture

### Frontend Architecture
- **Framework**: React 18 with TypeScript and Vite
- **UI Library**: shadcn/ui components built on Radix UI
- **Styling**: Tailwind CSS with dark mode support via theme provider
- **Forms**: react-hook-form with Zod validation
- **HTTP Client**: Axios for API requests
- **Routing**: react-router-dom (currently single route with disabled contact page)

**Key Frontend Paths**:
- Main entry: `src/frontend/src/main.tsx`
- Root component: `src/frontend/src/App.tsx`
- Form component: `src/frontend/src/components/InputForm/index.tsx`
- Form schema: `src/frontend/src/components/InputForm/schema.ts`
- Risk display: `src/frontend/src/components/RiskScore/index.tsx`
- UI components: `src/frontend/src/components/ui/` (shadcn components)
- Path alias: `@/` maps to `src/frontend/src/`

### Backend Architecture
- **Framework**: Django 4.2.7 with Django REST Framework (stateless API, no database)
- **ML Stack**: XGBoost + scikit-survival (Cox models) + SHAP + matplotlib

**Key Backend Paths**:
- Django project: `src/backend/fracture_risk/`
- API app: `src/backend/api/`
- ML module: `src/backend/fracture_risk/ml/`
- Risk calculator: `src/backend/fracture_risk/ml/risk_calculator.py`
- ML models: `src/backend/fracture_risk/ml/models/` (6 model files: 3 XGB + 3 Cox)
- SHAP plotting: `src/backend/fracture_risk/ml/plots/waterfall.py`

### Data Flow
1. User fills form in `InputForm` component with patient risk factors
2. Form validates using Zod schema and sends POST request to `/api/getRisk/`
3. Backend `getRisk` view validates data using `PatientSerializer` (validation only, no database persistence)
4. `BonoAI` class loads pre-trained models and prepares patient data:
   - Calculates BMI from height/weight
   - Derives `hrt` feature from `hrt_prior` and `hrt_current`
   - Renames features to match model training format
   - Calculates `min_tscore` from neck, total hip, and lumbar spine T-scores
   - Adds `No_treatment` flag
5. Risk calculation uses two-stage prediction:
   - XGBoost predicts risk score
   - Cox model converts score to time-dependent survival probability
6. SHAP plots generated separately via `/api/getShapPlot/` endpoint
7. Frontend displays risks and allows viewing SHAP plots for each fracture type

### Models and ML
- **Three fracture types**: vertebral, hip, any
- **Each type has two models**: XGBoost (`.json`) and Cox proportional hazards (`.pkl`)
- **Prediction pipeline**: XGB produces risk score → Cox model produces survival probability
- **SHAP values**: Computed using XGBoost explainer, rendered as custom waterfall plots
- **Feature engineering**: The `prepare_data` method performs critical transformations including feature renaming, BMI calculation, and derived features

## Environment Configuration

### Frontend Environment Variables
- `VITE_*` prefix for exposed variables
- Production API URL: `https://fracture-risk.onrender.com`
- Development API URL: `http://localhost:8000`

### Backend Environment Variables (`.env` in `src/backend/`)
- `DJANGO_SECRET_KEY`: Django secret key
- `AZURE_STORAGE_ACCOUNT_URL`: Azure blob storage URL
- `AZURE_STORAGE_ACCESS_TOKEN`: Azure access token
- `RENDER_EXTERNAL_HOSTNAME`: Set by Render.com in production
- `CORS_ALLOWED_ORIGINS`: Already configured in settings.py for localhost:5173 and production domains

## Patient Data Validation

The `PatientSerializer` (`src/backend/api/serializers.py`) validates patient risk factors:
- Demographics: sex, age, height, weight, bmi
- Family history: hip_fracture_parents, osteoporotic_fracture_parents
- Medical conditions: 15+ boolean fields for conditions (COPD, diabetes, arthritis, etc.)
- Medications: corticosteroids, aromatase_inhibitors, antiepileptics
- Lifestyle: alcohol, nicotin (smoking), number_of_falls, immobility
- Bone measurements: tscore_neck, tscore_total_hip, tscore_ls, tbs
- Fracture history: previous_fracture, recent_fracture (counts)
- Treatment history: 5 treatment types × 3 states (prior/current/new) = 15 boolean fields
  - Treatments: bisphosphonate, denosumab, serm, teriparatide, hrt

**Note**: This is a stateless API. Patient data is validated but NOT persisted to any database. Each request is independent.

## Key Implementation Details

### Feature Name Transformations
The backend performs critical feature renaming in `prepare_data()`:
- `antiepileptics` → `antiepileptic_drugs`
- `tscore_total_hip` → `tscore_totalHip`
- `tbs` → `tbs_ls`
- Treatment fields: lowercase to capitalized (e.g., `bisphosphonate_prior` → `Bisphosphonat_prior`)

### Treatment History Logic
- **Warning**: The model indicates prior bisphosphonate/denosumab treatment may increase fracture risk (counter to clinical trials)
- Treatment inputs: three checkboxes per treatment (Prior/Current/New)
- HRT feature is derived: `hrt = 1` if either `hrt_prior` or `hrt_current` is true

### SHAP Plot Generation
- Uses custom waterfall plot implementation (not default SHAP)
- Located in `src/backend/fracture_risk/ml/plots/waterfall.py`
- Returns base64-encoded PNG image
- Fetched separately from risk scores (one API call per fracture type)
- Frontend shows skeleton loader while SHAP plot is being generated

### CORS Configuration
Configured in `src/backend/fracture_risk/settings.py`:
- Development: `http://localhost:5173`
- Production: `https://bonoai-frontend.onrender.com`, `https://bonoai.ch`, `https://www.bonoai.ch`

## Deployment

Both frontend and backend deploy to Render.com:
- Configuration: `render.yaml` in root
- Backend uses Gunicorn WSGI server
- Frontend uses static site deployment
- No database required (stateless API)

## Current State

- Contact page is disabled (commented out in routes)
- Production URLs point to bonoai.ch domain
- Risk horizons: 1-7 years (selectable in UI, converted to months for model)
- Default risk horizon: 2 years
