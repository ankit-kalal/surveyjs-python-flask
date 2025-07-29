import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, Any, List
import uvicorn
from inmemorydbadapter import InMemoryDBAdapter

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

# In-memory session storage (simplified version)
session_storage = {}

def get_db_adapter():
    return InMemoryDBAdapter(session_storage)

API_BASE_ADDRESS = "/api"

@app.get(f"{API_BASE_ADDRESS}/getActive")
async def get_active():
    db = get_db_adapter()
    return db.get_surveys()

@app.get(f"{API_BASE_ADDRESS}/getSurvey")
async def get_survey(surveyId: str):
    db = get_db_adapter()
    survey = db.get_survey(surveyId)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey

@app.get(f"{API_BASE_ADDRESS}/changeName")
async def change_name(id: str, name: str):
    db = get_db_adapter()
    survey = db.change_name(id, name)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey

@app.get(f"{API_BASE_ADDRESS}/create")
async def create(name: Optional[str] = None):
    db = get_db_adapter()
    return db.add_survey(name)

@app.post(f"{API_BASE_ADDRESS}/changeJson")
async def change_json(request: Request):
    data = await request.json()
    db = get_db_adapter()
    return db.store_survey(data.get("id"), None, data.get("json"))

@app.post(f"{API_BASE_ADDRESS}/post")
async def post_results(request: Request):
    data = await request.json()
    db = get_db_adapter()
    return db.post_results(data.get("postId"), data.get("surveyResult"))

@app.get(f"{API_BASE_ADDRESS}/delete")
async def delete(id: str):
    db = get_db_adapter()
    survey = db.delete_survey(id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    return {"id": id}

@app.get(f"{API_BASE_ADDRESS}/results")
async def get_results(postId: str):
    db = get_db_adapter()
    results = db.get_results(postId)
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