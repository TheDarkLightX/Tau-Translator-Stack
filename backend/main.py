import os, json, asyncio
from typing import AsyncGenerator
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from openai import AsyncOpenAI
from utils import model_chain, parse_ok, run_tau

limiter = Limiter(key_func=get_remote_address, default_limits=[f"{os.getenv('RATE_LIMIT','60')}/minute"])
app = FastAPI(title="Tau‑Bridge")
app.state.limiter = limiter
client = AsyncOpenAI()
SYSTEM_PROMPT = (
    "You are a senior Tau‑Lang engineer. Translate the user’s English "
    "requirements into a fully‑formed, executable Tau specification. "
    "Reply with only the Tau code."
)

@app.post("/v1/translate")
@limiter.limit("10/minute")
async def translate(req: Request):
    data = await req.json()
    english = data.get("english", "").strip()
    if not english:
        raise HTTPException(400, "'english' required")

    model = await model_chain(client)
    stream = await client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": english}],
        temperature=0.2,
        stream=True,
    )

    async def event_stream() -> AsyncGenerator[str, None]:
        tau_buf = ""
        async for part in stream:
            frag = part.choices[0].delta.content or ""
            tau_buf += frag
            yield f"event: tau\ndata: {json.dumps({'chunk': frag})}\n\n"
        if not parse_ok(tau_buf):
            yield "event: error\ndata: invalid spec\n\n"
        else:
            yield "event: done\ndata: ok\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.post("/v1/execute")
@limiter.limit("10/minute")
async def execute(req: Request):
    data = await req.json()
    tau_code = data.get("tau", "")
    if not parse_ok(tau_code):
        raise HTTPException(400, "Invalid Tau spec")

    async def event_stream() -> AsyncGenerator[str, None]:
        async for line in run_tau(tau_code):
            yield f"data: {json.dumps({'out': line})}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")
