#os.environ.get('openai')
"""
230508 by O. Person & D. Masley
TODO:
* check history size so that it doesn't overflow API
* summarizing chat history
* endpoint for loading history
"""
import os
from fastapi import FastAPI, Depends
import openai, asyncio
from fastapi.middleware.cors import CORSMiddleware

openai.api_key = os.environ.get('openaikey')
model = 'gpt-3.5-turbo'
metaprompt = lambda x: f"You are the AI of this space ship. Keep your response short, time is limited! The persona that defines your character and tasks is given enclosed by >>><<< here >>>{x}<<<. You are to follow that persona directly and respond with your own short message. Here is the chat so far:"
history = []

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:8080"
    # Add any other origins you need to allow
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

log = print

prompt = "You will respond shortly, helpful and wittingly, throwing is smart jokes where appropriate to keep the morale up. Your response shall never be longer than 30 words. You shall being every response with a short well-structured JSON with populated fields: emotions (a list of user's emotions in last message), entities (list of named entities in user's text) and topic (a list with what is user's last message about)."
counter_lock = asyncio.Lock()
counter = 0
request_limit = 100

async def counter_dependency():
    return counter

@app.get("/persona")
async def update(text: str):
    global prompt
    global counter
    prompt = text
    response_text = {"message": "Persona updated successfully", "new_persona": text}
    log(counter, text)
    return response_text

@app.get("/complete")
async def complete(text: str, counter: int = Depends(counter_dependency)):
    global history
    global prompt
    history.append({"role":"user", "content":text})
    async with counter_lock:
        counter += 1
        if counter > request_limit:
            return {"error": f"This endpoint is no longer available after {request_limit} requests."}
    openai_response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role":"system","content":metaprompt(prompt)}]+history[-14:]
    )
    response_text = openai_response.choices[0].message.content
    history.append({"role":"assistant","content":response_text})
    log(counter, history)
    return response_text

@app.get("/status")
async def status():
    global prompt
    global counter
    global history
    response_text = {"message": "Printing current status", "prompt": prompt, "counter": counter, "history": history}
    return response_text

@app.post("/update_history")
async def update_history(uploaded_history: list):
    global history
    history = uploaded_history
    response_text = {"message": "Chat history updated successfully", "new_history": history}
    log(history)
    return response_text

@app.post("/update_status")
async def update_history(uploaded_status: dict):
    global history
    history = uploaded_status['history']
    response_text = {"message": "Chat history updated successfully", "new_history": history}
    log(history)
    return response_text