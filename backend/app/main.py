import uuid
import time
import logging
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import get_settings
from app.auth import verify_api_key
from app.limiter import limiter
from app.routers import symptoms, drugs, patients, graph, analysis
from app.dependencies import get_tg_service

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

settings = get_settings()

if settings.medgraph_api_key == "dev-insecure-key-change-me":
    logger.warning("Using default API key — set MEDGRAPH_API_KEY before deploying to production!")

app = FastAPI(
    title="MedGraph AI API",
    description="Healthcare Knowledge Graph powered by TigerGraph",
    version="2.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = [o.strip() for o in settings.allowed_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-API-Key"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    req_id = str(uuid.uuid4())[:8]
    start = time.time()
    response = await call_next(request)
    duration_ms = (time.time() - start) * 1000
    logger.info(
        "[%s] %s %s → %d (%.1fms)",
        req_id, request.method, request.url.path, response.status_code, duration_ms,
    )
    response.headers["X-Request-ID"] = req_id
    return response


_auth = [Depends(verify_api_key)]

app.include_router(symptoms.router,  prefix="/api/symptoms",  tags=["symptoms"],  dependencies=_auth)
app.include_router(drugs.router,     prefix="/api/drugs",     tags=["drugs"],     dependencies=_auth)
app.include_router(patients.router,  prefix="/api/patients",  tags=["patients"],  dependencies=_auth)
app.include_router(graph.router,     prefix="/api/graph",     tags=["graph"],     dependencies=_auth)
app.include_router(analysis.router,  prefix="/api/patients",  tags=["analysis"],  dependencies=_auth)


@app.get("/")
def root():
    return {"message": "MedGraph AI API", "status": "running", "version": app.version}


@app.get("/health")
def health(tg=Depends(get_tg_service)):
    db_ok = tg.conn is not None
    return {
        "status": "healthy" if db_ok else "degraded",
        "database": "connected" if db_ok else "disconnected",
        "version": app.version,
    }
