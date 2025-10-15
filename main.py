import os
import httpx
from mangum import Mangum
from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse

app = FastAPI()
WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL")

@app.get("/callback")
async def callback(
    sender: str = Query(...),
    receiver: str = Query(...),
    kind: int = Query(..., description="1=전화, 2=SMS"),
    inner_num: str | None = Query(None),
    message: str | None = Query(None),
):
    if not WEBHOOK:
        return PlainTextResponse("DISCORD_WEBHOOK_URL not set", status_code=500)

    text = (
        f"[Centrex]\n"
        f"- kind: {kind}\n"
        f"- sender: {sender}\n"
        f"- receiver: {receiver}\n"
        f"- inner_num: {inner_num or '-'}\n"
        f"- message: {message or '-'}"
    )

    async with httpx.AsyncClient(timeout=5) as c:
        await c.post(WEBHOOK, json={"content": text})

    return "OK"

handler = Mangum(app, lifespan="off")