# SurveyJS + FastAPI Demo Example

This demo shows how to integrate SurveyJS components with a Python backend using the FastAPI framework.

## Features

- **FastAPI Backend**: Modern, fast web framework for building APIs with Python
- **SurveyJS Integration**: Full integration with SurveyJS survey components
- **In-Memory Storage**: Simple in-memory database for demo purposes
- **CORS Support**: Configured for cross-origin requests
- **Static File Serving**: Serves the React frontend application

## Run the Application

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the FastAPI application:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. Open http://localhost:8000 in your web browser.

## API Endpoints

The FastAPI application provides the following endpoints:

- `GET /api/getActive` - Get all active surveys
- `GET /api/getSurvey?surveyId={id}` - Get a specific survey
- `GET /api/changeName?id={id}&name={name}` - Change survey name
- `GET /api/create?name={name}` - Create a new survey
- `POST /api/changeJson` - Update survey JSON data
- `POST /api/post` - Post survey results
- `GET /api/delete?id={id}` - Delete a survey
- `GET /api/results?postId={id}` - Get survey results

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
├── main.py                 # FastAPI application
├── inmemorydbadapter.py    # Database adapter
├── demo_surveys.py         # Demo survey data
├── requirements.txt         # Python dependencies
├── public/                 # Frontend static files
│   ├── index.html         # Main HTML file
│   └── static/            # Static assets
└── README_FASTAPI.md      # This file
```

## Differences from Flask Version

- Uses FastAPI instead of Flask
- Async/await support for better performance
- Automatic API documentation with Swagger/OpenAPI
- Pydantic models for request/response validation
- Simplified session storage (in-memory dictionary)
- CORS middleware included
- Better error handling with HTTPException

## Disclaimer

This demo must not be used as a real service as it doesn't cover such real-world survey service aspects as authentication, authorization, user management, access levels, and different security issues. These aspects are covered by backend-specific articles, forums, and documentation.

## About

This demo shows how to integrate SurveyJS components with a Python backend using the FastAPI framework. 