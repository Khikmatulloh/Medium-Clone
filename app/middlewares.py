import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class RequestTimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(f"{request.method} {request.url.path} completed in {process_time:.2f} ms")
        response.headers["X-Process-Time-ms"] = f"{process_time:.2f}"
        return response



def setup_cors(app):
    origins = [
        "http://localhost:3000",
        "https://your-frontend.com"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
