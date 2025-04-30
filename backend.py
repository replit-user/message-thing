from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  # Add this import

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (update for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

users = {}
original_messages = []
copied_messages = []

# ... rest of your existing endpoints remain unchanged ...
@app.post("/signup")
async def signup(username: str = Body(...), password: str = Body(...)):
    if username in users:
        return JSONResponse(content={"success": False}, status_code=400)
    users[username] = {"password": password, "messages": 10, "points": 0}
    return JSONResponse(content={"success": True}, status_code=200)

# ... keep all other endpoints the same ...
