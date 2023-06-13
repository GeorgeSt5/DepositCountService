import uvicorn

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from fastapi.exceptions import RequestValidationError

from fastapi.responses import JSONResponse
from routers import router_api


app = FastAPI(
    title='Deposit count app',
    description='Система для рассчёта депозита',
    version='0.0.1'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# дрбавление роутера рассчёта
def configure_fastapi():
    app.include_router(router_api)


# кастомизированный хэндлер валидационной ошибки
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "error": str(exc)},
    )


# хэндлер базовой ошибки
@app.exception_handler(Exception)
async def other_error_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc)},
    )

# запуск вэб-сервера
if __name__ == '__main__':
    configure_fastapi()
    uvicorn.run(
        'main:app',
        host="0.0.0.0",
        port=8000,
        reload=True
    )
else:
    configure_fastapi()
