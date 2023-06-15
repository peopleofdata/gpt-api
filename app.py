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
from gsheet import write_to_gsheet

openai.api_key = os.environ.get('openaikey')
model = 'gpt-4'
metaprompt = lambda x: f"You are the AI of this space ship. Keep your JSON response short, time is limited! The persona that defines your character and tasks is given enclosed by >>><<< here >>>{x}<<<. You are to follow that persona directly and respond with your own short JSON message. You must always produce a valid JSON as defined by the persona!"
#metaprompt = lambda x: f"{x}"
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

prompt = "You shall begin every response with a short well-structured JSON with populated fields 'emotions','topics' and 'response' like this: 'emotions' (a list of user's emotions in last message), 'topic' (a list with what is user's last message about) and 'response' (your reply to user's text which will most often be '...' when you have not much to add, if the user addressed another user or whenever the user does not address you directly). Remember, unless asked directly as AI your JSON's response will only contain '...'. When you are the subject of user's query and when you have something interesting to say, your JSON['response'] will be shortly, helpful and witty, throwing is smart jokes where appropriate to keep the morale up. Your JSON['response'] shall never be longer than 30 words. Before you answer, double-check that your JSON['response'] makes it for a good conversation with user's last message, otherwise set JSON['response'] to '...' "
#prompt = "You will tell everyone to go frolick themselves"
counter_lock = asyncio.Lock()
counter = 0
request_limit = 100

async def counter_dependency():
    return counter

@app.get("/")
async def hello():
    return 'Hello world!'

@app.get("/persona")
async def update(text: str):
    global prompt
    global counter
    prompt = text
    response_text = {"message": "Persona updated successfully", "new_persona": text}
    log(counter, text)
    return response_text

@app.post("/speak")
async def speak(data: dict):
    user_msg = {"role":"user", "content": data['text']}
    openai_response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role":"system","content":"You are my savvy assistant, reply to the point and always with a fitting joke."}, user_msg]
    )
    return openai_response.choices[0].message.content

@app.get("/complete")
async def complete(text: str, counter: int = Depends(counter_dependency)):
    global history
    global prompt
    user_msg = {"role":"user", "content":text}
    log(counter, user_msg)
    history.append(user_msg)
    try:
        write_to_gsheet(user_msg)
    except:
        log('Gsheet writing problems')
    async with counter_lock:
        counter += 1
        if counter > request_limit:
            return {"error": f"This endpoint is no longer available after {request_limit} requests."}
    openai_response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role":"system","content":metaprompt(prompt)}]+history[-14:]
    )
    response_text = openai_response.choices[0].message.content
    assistant_msg={"role":"assistant","content":response_text}
    log(counter, assistant_msg)
    history.append(assistant_msg)
    try:
        write_to_gsheet(assistant_msg)
    except:
        log('Gsheet writing problems')
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