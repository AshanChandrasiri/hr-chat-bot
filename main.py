import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from controllers.chat import chat_controller
from utils.bootstrap_runner import lifespan

load_dotenv()
app = FastAPI(title="ASK Git", description="A tool to ask questions about GitHub repositories.", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_controller(app)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
