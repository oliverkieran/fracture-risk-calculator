# Bono AI

> [!NOTE]
> This branch is currently not active.
> Reason: Deployment to Azure Static Web Apps currently doesn't work because of their 100MB app size limit (last checked: 20.04.2024). The .venv folder of the api is too large for the deployment. Azure reported to increase the limit in the future.

## Introduction

This is the source code of Bono AI, a machine learning project that aims to compute 2-year fracture risk for postmenopausal women. It includes a website, that lets users compute fracture risks by inputing the required risk factors, and provides further insights into the risk score calculations by displaying SHAP plots. The website will soon be available at [bonoai.ch](https://bonoai.ch).

## Installation

### Frontend

- Navigate to the `frontend` folder with `cd frontend`
- Install the dependencies with `npm install`
- Start the development server with `npm start dev`

### Backend

- Navigate to the `backend` folder with `cd backend`
- Create a virtual environment and install all the required dependencies.
- Setup a local PostgreSQL database and create a new database. You can follow the steps [here](https://djangocentral.com/using-postgresql-with-django/).
- Create a `.env` file in the `backend` folder and add the following environment variables: `DB_NAME`, `DB_USER`, `DB_PASSWORD` and `DB_HOST`. The values of these variables should be the same as the ones you used when setting up the PostgreSQL database.
- Run the migrations with `python manage.py migrate`
- Start the development server with `python manage.py runserver`

> [!IMPORTANT]
> Make sure to set the `CORS_ALLOWED_ORIGINS` variable in the `backend/fracture_risk/settings.py` to the address of the frontend. This is necessary to allow cross-origin requests and ensure proper communication between the frontend and backend.

## Architecture

### Frontend

The frontend is built with [React](https://react.dev/), TypeScript and [shadcn/ui](https://ui.shadcn.com/). Requests to the backend are made with [Axios](https://axios-http.com/).

### Backend

The backend is built with [Django](https://www.djangoproject.com/). The backend will expose an API via [Django Rest Framework](https://www.django-rest-framework.org/) which will give the frontend the necessary endpoints to request risk scores or SHAP plots. The backend is also responsible for storing the risk scores in a PostgreSQL database. More information on how to install and setup Django with PostgreSQL can be found [here](https://djangocentral.com/using-postgresql-with-django/).

#### Dependencies

- pandas
- numpy
- xgboost
- sksurv
- shap
- django
- django-rest-framework
- django-cors-headers
- psycopg2
- gunicorn

### Deployment

The frontend and the backend are deployed separately. Both are deployed on [render](https://render.com/).

## Notes

- This project is currently being developed. Thus there will be many updates in the near future so make sure to check back frequently.

## Contact

If you have any questions or suggestions, feel free to contact me at [lehmannoliver96@gmail.com](mailto:lehmannoliver96@gmail.com)
