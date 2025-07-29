# SurveyJS + FastAPI Demo Example

This demo shows how to integrate SurveyJS components with a Python backend using the FastAPI framework with SQLite database.

## Features

- **FastAPI Backend**: Modern, fast web framework for building APIs with Python
- **SQLite Database**: Persistent data storage with automatic initialization
- **SurveyJS Integration**: Full integration with SurveyJS survey components
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

## Database

The application uses SQLite database (`surveyjs.db`) for persistent data storage:

- **Automatic Initialization**: Database and tables are created automatically on first run
- **Demo Data**: Pre-populated with sample surveys and results
- **Persistent Storage**: Data persists between application restarts
- **SQLite File**: Located at `surveyjs.db` in the project root

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
├── sqlitedbadapter.py      # SQLite database adapter
├── inmemorydbadapter.py    # In-memory database adapter (legacy)
├── demo_surveys.py         # Demo survey data
├── requirements.txt         # Python dependencies
├── surveyjs.db             # SQLite database file (created automatically)
├── public/                 # Frontend static files
│   ├── index.html         # Main HTML file
│   └── static/            # Static assets
└── README_FASTAPI.md      # This file
```

## Database Schema

### Surveys Table
- `id` (TEXT PRIMARY KEY): Survey identifier
- `name` (TEXT NOT NULL): Survey name
- `json_data` (TEXT): Survey JSON configuration

### Results Table
- `id` (TEXT PRIMARY KEY): Result identifier
- `data` (TEXT): JSON array of survey results

## Differences from Flask Version

- Uses FastAPI instead of Flask
- SQLite database instead of in-memory storage
- Async/await support for better performance
- Automatic API documentation with Swagger/OpenAPI
- Better error handling with HTTPException
- CORS middleware included
- Persistent data storage

## Disclaimer

This demo must not be used as a real service as it doesn't cover such real-world survey service aspects as authentication, authorization, user management, access levels, and different security issues. These aspects are covered by backend-specific articles, forums, and documentation.

## About

This demo shows how to integrate SurveyJS components with a Python backend using the FastAPI framework with SQLite database. 