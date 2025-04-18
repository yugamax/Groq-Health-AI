import os
from groq import Groq
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio

os.environ["GROQ_API_KEY"] = "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"

client= Groq()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)


class UserMessage(BaseModel):
    msg : str

chat_hist= [{"role": "system", "content": "You are a smart AI doctor."}]

@app.api_route("/ping", methods=["GET", "HEAD"])
async def ping():
    await asyncio.sleep(0.1)
    return {"message": "server is running"}

@app.post("/chat")
async def chat_with_doctor(ui: UserMessage):
    ui = ui.msg
    if ui.lower() in ["bye", "exit", "quit"]:
        return {"response": "Bye"}

    chat_hist.append({"role": "user", "content": ui})

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=chat_hist,
            temperature=0.7,
            max_tokens=512,
        )
        res = completion.choices[0].message.content
        chat_hist.append({"role": "assistant", "content": res})
        return {"response":res}
    
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)