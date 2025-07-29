import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, Any, List
import uvicorn
from sqlitedbadapter import SQLiteDBAdapter

app = FastAPI(title="SurveyJS FastAPI Service", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="public/static"), name="static")

# SQLite database adapter
db_adapter = SQLiteDBAdapter("surveyjs.db")

API_BASE_ADDRESS = "/api"

@app.get(f"{API_BASE_ADDRESS}/getActive")
async def get_active():
    return db_adapter.get_surveys()

@app.get(f"{API_BASE_ADDRESS}/getSurvey")
async def get_survey(surveyId: str):
    survey = db_adapter.get_survey(surveyId)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey

@app.get(f"{API_BASE_ADDRESS}/changeName")
async def change_name(id: str, name: str):
    survey = db_adapter.change_name(id, name)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey

@app.get(f"{API_BASE_ADDRESS}/create")
async def create(name: Optional[str] = None):
    return db_adapter.add_survey(name)

@app.post(f"{API_BASE_ADDRESS}/changeJson")
async def change_json(request: Request):
    data = await request.json()
    return db_adapter.store_survey(data.get("id"), None, data.get("json"))

@app.post(f"{API_BASE_ADDRESS}/post")
async def post_results(request: Request):
    data = await request.json()
    return db_adapter.post_results(data.get("postId"), data.get("surveyResult"))

@app.get(f"{API_BASE_ADDRESS}/delete")
async def delete(id: str):
    survey = db_adapter.delete_survey(id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    return {"id": id}

@app.get(f"{API_BASE_ADDRESS}/results")
async def get_results(postId: str):
    results = db_adapter.get_results(postId)
    if not results:
        raise HTTPException(status_code=404, detail="Results not found")
    return results

# Serve the React app for all other routes
@app.get("/{full_path:path}")
async def serve_static(full_path: str):
    # Serve index.html for all routes to support React Router
    return FileResponse("public/index.html")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 