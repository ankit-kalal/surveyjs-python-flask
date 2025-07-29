# SurveyJS + FastAPI Demo Example

This demo shows how to integrate SurveyJS components with a Python backend using the FastAPI framework.

View Demo Online

## Disclaimer

This demo must not be used as a real service as it doesn't cover such real-world survey service aspects as authentication, authorization, user management, access levels, and different security issues. These aspects are covered by backend-specific articles, forums, and documentation.

## Run the Application

Install Python dependencies and run the application:

```bash
pip install -r requirements.txt
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open http://localhost:8000 in your web browser.

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Client-Side App

The client-side part is the `surveyjs-react-client` React application. The current project includes only the application's build artifacts. Refer to the surveyjs-react-client repo for full code and information about the application.

## About

This demo shows how to integrate SurveyJS components with a Python backend using the FastAPI framework.
