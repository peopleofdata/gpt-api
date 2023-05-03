#os.environ.get('openai')
import os
from fastapi import FastAPI
import openai, asyncio
from fastapi.middleware.cors import CORSMiddleware

openai.api_key = os.environ.get('openai')
model = 'gpt-3.5-turbo'
prompt = "Keep your response short, time is limited! You are on a spaceship, stranded, without hope..."

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

counter_lock = asyncio.Lock()
counter = 0
request_limit = 100

@app.get("/persona")
async def update(text: str):
    global prompt
    global counter
    prompt = text
    response_text = {"message": "Persona updated successfully", "new_persona": text}
    log(counter, text)
    return response_text

@app.get("/complete")
async def complete(text: str):
    global counter
    async with counter_lock:
        counter += 1
        if counter > request_limit:
            return {"error": f"This endpoint is no longer available after {request_limit} requests."}

    openai_response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ]
    )

    log(counter, text)
    response_text = {"response": openai_response.choices[0].message.content}
    return response_text