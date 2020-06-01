from fastapi import FastAPI, Request, Response
from starlette.middleware.cors import CORSMiddleware
from book import app as app_book
from db import session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # TODO CORS URLS
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def index():
    return {
        'msg': ':bird: 33-4 :tiger:'
    }


app.include_router(
    app_book.api,
    prefix='/book',
    tags=['book']
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = session()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8080)
