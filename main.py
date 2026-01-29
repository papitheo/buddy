# main.py
# The web framework for building the API
from fastapi import FastAPI
# Handles Cross-Origin Resource Sharing for frontend access
from fastapi.middleware.cors import CORSMiddleware
# For POST request validation and response verification
from pydantic import BaseModel
# HTTP client for making requests to Ollama
import request

# The API endpoint for the local Ollama AI service
OLLAMA_URL = "http://localhost:11434/api/chat"

# creates a fast API application instance 
app = FastAPI()

# define a list of allowed URLs for Cross-Origin Resource Sharing (CORS).
# i.e the list of URLs that can share information with your URL
# origins lists URLs permitted to make requests to your API
# adds special HTTP headers to API responses telling the browser: 
# "Yes, it's okay for frontend apps running at these URLs to access this API
# origins all for the  CORS operation
origins = [
    # typically used by React development servers
    "http://localhost:3000",
    # the default port for Vite development servers
    "http://localhost:5173",
]

# Intecepts all incoming requesta and adds appropriate CORS headers to responses
app.add_middleware(
    # The type of middleware that we are specifying
    CORSMiddleware,
    # (origin parameter) The allowed URLs that should be allowed 
    allow_origins=origins,
    # (credentials parameter) Allows the frontend to send credentials 
    # (cookies, authorization headers, TLS client certificates)
    allow_credentials=True,
    # (methods parameter) The * wildcard means all HTTP methods are allowed (GET, POST, PUT, DELETE, PATCH, etc.)
    allow_methods=["*"],
    # The * wildcard means all HTTP headers are allowed in requests
    # The frontend can send custom headers (like Authorization, Content-Type, etc.)
    allow_headers=["*"],
)



# This code defines a data validation model for incoming chat requests.
#Creates a Pydantic model that defines the structure of JSON data your API expects to receive. 
# It inherits from BaseModel to gain validation superpowers.
class ChatRequest(BaseModel):
    # Required field. Comtains the user's chat message and must be provided in evevry request
    # fastAPI will reject the request without this field 
    message: str
    # List of dictionaries. each dic is a conversation history. It is optional.
    # It can either be a list of dictionalries or none
    history: list[dict] | None = None

# The response is a string
class ChatResponse(BaseModel):
    reply: str


# This function is called  when a GET request is made the root path (/) 
# Provided the URL is http://localhost:8000/, when a GET request is made to this root path, this fucntion is called.
@app.get("/")
def read_root():
    # Returns a JSON response indicating the API is running and healthy
    return {"status": "ok"}

# @app.post("/chat"): This is a decorator registering a POST endpoint "chat" route
# when frontend sends a POST to http://localhost:11434/chat, this function is executed
# response_model=ChatResponse: Validates the chatResponse against the chatResponse model
@app.post("/chat", response_model=ChatResponse)
# async allows for multiple requests to be made while the API is handling a request 
# req: ChatRequest: Here, fastAPI automatically validates incoming requests against chatRequest model, 
# and retrun error if validation fails 
async def chat(req: ChatRequest):
    # Retrieve history from the chatRequest, if any
    messages = req.history or []
    # Append the users query to the history retrieved
    messages.append({"role": "user", "content": req.message})

# JSON body that would be sent to your API
    payload = {
        "model": "gemma3",
        "messages": messages,
        "stream": False,
    }

    # Sends HTTP POST request(payload) to API (OLLAMA- local LLM)
    # json=payload: Converts payload dict to json
    # r stores the response obj
    r = request.post(OLLAMA_URL, json=payload)
    # Checks if the HTTP response was succesfull, and raises an exception if any error occurs
    # Prevents it from processing invalid response
    r.raise_for_status()
    # Assign the response as dictionary other than a JSON to data
    data = r.json()
    # Extract the content from the message 
    reply_text = data["message"]["content"]
    # Return the reply 
    return ChatResponse(reply=reply_text)
