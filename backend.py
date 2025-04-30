from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse

app = FastAPI()

users = {}
original_messages = []
copied_messages = []

@app.post("/signup")
async def signup(username: str = Body(...), password: str = Body(...)):
    if username in users:
        return JSONResponse(content={"success": False}, status_code=400)
    users[username] = {"password": password, "messages": 10, "points": 0}
    return JSONResponse(content={"success": True}, status_code=200)

@app.post("/signin")
async def signin(username: str = Body(...), password: str = Body(...)):
    if username not in users or users[username]["password"] != password:
        return JSONResponse(content={"success": False}, status_code=401)
    return JSONResponse(content={"success": True}, status_code=200)

@app.post("/original")
async def send_original_message(username: str = Body(...), message: str = Body(...)):
    if username not in users or users[username]["messages"] <= 0:
        return JSONResponse(content={"success": False}, status_code=401)
    original_messages.append({"username": username, "message": message})
    users[username]["messages"] -= 1
    return JSONResponse(content={"success": True}, status_code=200)

@app.post("/copied")
async def send_copied_message(message: str = Body(...)):
    success = False
    for original_message in original_messages:
        if message == original_message:
            success = True
            break
    if not success:
        return JSONResponse(content={"success": False}, status_code=401)
    copied_messages.append(message)
    return JSONResponse(content={"success": True}, status_code=200)

@app.get("/messages/{type}")
def get_messages(type: str):
    if type == "original":
        return JSONResponse(content=original_messages, status_code=200)
    elif type == "copied":
        return JSONResponse(content=copied_messages, status_code=200)
    else:
        return JSONResponse(content={"success": False}, status_code=400)

@app.post("/redeem")
def redeem_message(username: str = Body(...)):
    if username not in users or users[username]["points"] < 100:
        return JSONResponse(content={"success": False}, status_code=401)
    users[username]["points"] -= 100
    users[username]["messages"] += 1
    return JSONResponse(content={"success": True}, status_code=200)