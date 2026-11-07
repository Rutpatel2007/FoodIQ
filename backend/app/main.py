"""
FoodIQ Competitive Intelligence Engine - FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.api.v1 import (
    health,
    companies,
    documents,
    segments,
    metrics,
    observations,
    data_quality,
    comparability,
    guidance
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Research-grade financial and competitive intelligence engine for Eternal Limited and Swiggy Limited disclosures.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for Next.js frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register v1 API routes
app.include_router(health.router, prefix=settings.API_V1_PREFIX, tags=["System Health"])
app.include_router(companies.router, prefix=settings.API_V1_PREFIX, tags=["Companies"])
app.include_router(documents.router, prefix=settings.API_V1_PREFIX, tags=["Source Documents"])
app.include_router(segments.router, prefix=settings.API_V1_PREFIX, tags=["Business Segments"])
app.include_router(metrics.router, prefix=settings.API_V1_PREFIX, tags=["Metric Definitions"])
app.include_router(observations.router, prefix=settings.API_V1_PREFIX, tags=["Metric Observations & Lineage"])
app.include_router(data_quality.router, prefix=settings.API_V1_PREFIX, tags=["Data Quality & Integrity"])
app.include_router(comparability.router, prefix=settings.API_V1_PREFIX, tags=["Financial Governance & Comparability"])
app.include_router(guidance.router, prefix=settings.API_V1_PREFIX, tags=["Management Guidance & Commitments"])

@app.get("/")
def root():
    return {
        "message": "Welcome to FoodIQ Competitive Intelligence Engine API",
        "docs": "/docs",
        "version": "1.0.0"
    }
