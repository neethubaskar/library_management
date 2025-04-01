from fastapi import FastAPI
from routes import book, user, borrowing
import logging


app = FastAPI(title="Library Management System")

app.include_router(book.router)
app.include_router(user.router)
app.include_router(borrowing.router)


@app.get("/home/")
def root():
    return {"message": "Welcome to the Library Management System API"}


# Logging API requests
@app.middleware("http")
async def log_requests(request, call_next):
    response = await call_next(request)
    logging.info(f"Request: {request.method} {request.url}")
    return response
