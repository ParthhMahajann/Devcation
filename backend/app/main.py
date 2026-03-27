from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import symptoms, drugs, patients, graph

app = FastAPI(
    title="MedGraph AI API",
    description="Healthcare Knowledge Graph powered by TigerGraph",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(symptoms.router, prefix="/api/symptoms", tags=["symptoms"])
app.include_router(drugs.router,    prefix="/api/drugs",    tags=["drugs"])
app.include_router(patients.router, prefix="/api/patients", tags=["patients"])
app.include_router(graph.router,    prefix="/api/graph",    tags=["graph"])


@app.get("/")
def root():
    return {"message": "MedGraph AI API", "status": "running", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}
