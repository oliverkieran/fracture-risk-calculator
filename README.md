# Bono AI

## Introduction

This is the source code of Bono AI, a machine learning project that aims to compute 2-year fracture risk for postmenopausal women. It includes a website, that lets users compute fracture risks by inputing the required risk factors, and provides further insights into the risk score calculations by displaying SHAP plots. The website will soon be available at [bonoai.ch](https://bonoai.ch).

## Installation

- Clone the repository with `git clone`.

### Frontend

- Navigate to the `frontend` folder with `cd frontend`
- Install the dependencies with `npm install`
- Start the development server with `npm start dev`

## Architecture

### Frontend

The frontend is built with [React](https://react.dev/) and [shadcn/ui](https://ui.shadcn.com/). Requests to the backend are made with [Axios](https://axios-http.com/).

### Backend

The backend is built with [Django](https://www.djangoproject.com/). The backend will expose an API via [Django Rest Framework](https://www.django-rest-framework.org/) which will give the frontend the necessary endpoints to request risk scores or SHAP plots.

### Deployment

The website is planned to be deployed on a AWS EC2 instance, maybe including Docker, but this is not yet decided. I also want to investigate AWS Lambda and AWS API Gateway as a possible deployment option.

Another possibility is to deploy the website on [Heroku](https://www.heroku.com/).

## Notes

- Ignore the `backend` folder for now as it is not yet used.
