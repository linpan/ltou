from datetime import time
from typing import Callable
from starlette.requests import Request
from starlette.responses import Response


async def add_process_time_header(request: Request, call_next) -> Response:
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
