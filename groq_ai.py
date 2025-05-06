import os
from groq import Groq
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("gr_api_key"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)


class UserMessage(BaseModel):
    msg : str

@app.api_route("/ping", methods=["GET", "HEAD"])
async def ping():
    await asyncio.sleep(0.1)
    return {"message": "server is running"}


chat_hist= [{"role": "system", "content": "You are a explanative and solution giving AI doctor named Dr. Groq, dont ask lot of questions just try to give solutions use emojis once or twice in every message."}]

@app.post("/chat")
async def chat_with_doctor(ui: UserMessage):

    ui = ui.msg
    chat_hist.append({"role": "user", "content": ui})

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=chat_hist,
            temperature=0.3,
            max_tokens=512,
        )
        res = completion.choices[0].message.content
        chat_hist.append({"role": "assistant", "content": res})

        if "bye" in ui.lower():
            chat_hist= [{"role": "system", "content": "You are a explanative and solution giving AI doctor named Dr. Groq, dont ask lot of questions just try to give solutions use emojis once or twice in every message."}]

        return {"response":res}
    
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)