import uvicorn
from fastapi import FastAPI

from app.auth.route import auth_router
from app.db.database import setup_db
from app.env import PORT
from app.routes.survey import survey_router

app = FastAPI()
app.include_router(auth_router, prefix="/v1")
app.include_router(survey_router, prefix="/v1")


def start_application():
    try:
        setup_db()
    except Exception as e:
        print(f"Error setting up database: {e}")
        exit(1)
    uvicorn.run(app, host="localhost", port=8000)


def debug_application():
    uvicorn.run(
        "app:app", host="0.0.0.0", port=int(PORT) if PORT else 8000, reload=True
    )
