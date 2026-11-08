"""
FoodIQ Competitive Intelligence Engine - FastAPI Application
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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
    guidance,
    analytics,
    competitive,
    credibility,
    quantitative,
    scenarios,
    reports,
    disclosures,
    extensions
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
app.include_router(analytics.router, prefix=settings.API_V1_PREFIX, tags=["Financial Analytics & Decomposition Core"])
app.include_router(competitive.router, prefix=settings.API_V1_PREFIX, tags=["Competitive Intelligence & Structural Break Engine"])
app.include_router(credibility.router, prefix=settings.API_V1_PREFIX, tags=["Management Credibility & Narrative Verification"])
app.include_router(quantitative.router, prefix=settings.API_V1_PREFIX, tags=["Quantitative Research & Statistical Analysis"])
app.include_router(scenarios.router, prefix=settings.API_V1_PREFIX, tags=["Scenario Lab & Simulation"])
app.include_router(reports.router, prefix=settings.API_V1_PREFIX, tags=["Institutional Research Report Generation"])
app.include_router(disclosures.router, prefix=settings.API_V1_PREFIX, tags=["Corporate Disclosure Intelligence & Research Monitoring"])
app.include_router(extensions.router, prefix=settings.API_V1_PREFIX, tags=["Extensible Architecture & Plugins"])

# Mount static frontend files if frontend directory exists
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
def root():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "message": "Welcome to FoodIQ Competitive Intelligence Engine API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/api")
def api_info():
    return {
        "message": "FoodIQ Competitive Intelligence Engine API v1",
        "docs": "/docs",
        "version": "1.0.0"
    }
