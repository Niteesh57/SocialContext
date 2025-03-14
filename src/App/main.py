from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from src.Routes import posts, roles, roleMap, users

app = FastAPI(
    title="Social Context",
    description="This is a simple FastAPI app with Models, JWT",
    version="0.1.0",
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(roleMap.router, prefix="/roleMap", tags=["RoleMapping"])
app.include_router(roles.router, prefix="/roles", tags=["Roles"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])

@app.get('/')
async def read_root():
    return {"message": "Welcome, TO Social Context API!"}

