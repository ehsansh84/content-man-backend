import os, sys
import uvicorn
# from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
project_dir = os.getenv("PROJECT_DIR")
if project_dir:
    sys.path.append(project_dir)
from app.api.v1.user import router as user_router
from app.api.v1.content import router as content_router
from app.api.v1.category import router as category_router
from app.api.v1.privacy import router as privacy_router
from app.api.v1.health_check import router as health_check_router

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=user_router)
app.include_router(router=content_router)
app.include_router(router=category_router)
app.include_router(router=privacy_router)
app.include_router(router=health_check_router)
# app.mount("/static", StaticFiles(directory=Settings.MEDIA_PATH), name="static")
# app.mount("/uploaded", StaticFiles(directory=Settings.UPLOAD_PATH), name="uploaded")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8200, reload=True)
