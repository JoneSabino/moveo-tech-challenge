from fastapi import FastAPI, Request, Header
from models import response as res
from moveo_webhook import MoveoWebhookHandler

app = FastAPI()

WEBHOOK_SECRET = "eos3nx26om42a0b"


@app.post("/{path:path}")
async def handle_post(request: Request, x_moveo_signature: str = Header(None)):
    moveo_signature = x_moveo_signature
    try:
        request_body = await request.json()

        handler = MoveoWebhookHandler(WEBHOOK_SECRET, debug=True)
        return handler.process_request(request_body, moveo_signature)

    except Exception as e:
        return res.err_response(f"Exception occurred: {str(e)}").model_dump(exclude_none=True)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)
