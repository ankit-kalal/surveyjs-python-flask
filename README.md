# SurveyJS + Python/Flask Demo Example

This demo shows how to integrate [SurveyJS](https://surveyjs.io/) components with a Python/Flask backend.

[View Demo Online](https://surveyjs-flask.azurewebsites.net/)

## Disclaimer

This demo must not be used as a real service as it doesn't cover such real-world survey service aspects as authentication, authorization, user management, access levels, and different security issues. These aspects are covered by backend-specific articles, forums, and documentation.

## Run the Application

Install [NodeJS](https://nodejs.org/) on your machine. After that, run the following commands:

```bash
git clone https://github.com/surveyjs/surveyjs-flask.git
cd surveyjs-flask

# python -m venv .venv # create venv in working folder if needed - windows
# python3 -m venv .venv # macos/linux
pip install -r requirements.txt

```

Open http://localhost:5000 in your web browser.

## Client-Side App

The client-side part is the `surveyjs-react-client` React application. The current project includes only the application's build artifacts. Refer to the [surveyjs-react-client](https://github.com/surveyjs/surveyjs-react-client) repo for full code and information about the application.
