# FoodIQ Phase 9 — Environment Configuration Guide

## 1. Configuration Matrix

All configuration parameters are managed via environment variables or `.env` files:

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `FOODIQ_ENV` | `production` | Runtime mode: `production` or `development` |
| `HOST` | `127.0.0.1` | Network interface to bind |
| `PORT` | `8000` | Port for FastAPI service |
| `DATABASE_URL` | `sqlite:///data/foodiq.db` | SQLAlchemy connection string |
| `LOG_LEVEL` | `INFO` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `ALLOWED_HOSTS` | `*` | Allowed CORS origins |
| `REPORTS_STORAGE_DIR`| `data/reports/exports` | Export directory for HTML, PDF, DOCX, CSV reports |

---

## 2. Path Portability Assurance

The codebase enforces strict path portability:
- Resolves paths using `pathlib.Path(__file__).resolve().parent.parent.parent`.
- Zero machine-specific absolute usernames or developer paths in code.
- Compatible across Windows (`\` and drive letters), Linux (`/`), and macOS.
