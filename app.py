from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from book import app as app_book

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

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8080)
