from fastapi import FastAPI

from api_endpoints import webhook


app = FastAPI()
app.include_router(webhook.router)


@app.get("/health")
async def health():
    return {"status": "ok"}


