from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.search import router as search_router
from app.api.favorites import router as favorites_router
from app.core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("========================================")
    logger.info("TMDB SEARCH ENGINE STARTING")
    logger.info("========================================")

    yield

    logger.info("========================================")
    logger.info("TMDB SEARCH ENGINE STOPPING")
    logger.info("========================================")


app = FastAPI(
    title="TMDB Search Engine",
    version="1.0",
    lifespan=lifespan,
)

# --------------------------------------------------
# Templates
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"

logger.info(f"BASE_DIR      : {BASE_DIR}")
logger.info(f"TEMPLATE_DIR  : {TEMPLATE_DIR}")

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


# --------------------------------------------------
# Frontend Routes
# --------------------------------------------------


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/favorites", response_class=HTMLResponse)
async def read_favorites(request: Request):
    # Fixed the signature mismatch causing the unhashable dict type error
    return templates.TemplateResponse(request=request, name="favorites.html")


# --------------------------------------------------
# APIs Registration Blocks
# --------------------------------------------------

app.include_router(
    search_router,
    prefix="/api",
    tags=["Search"],
)

app.include_router(
    favorites_router,
    prefix="/api",
    tags=["Favorites"],
)

# --------------------------------------------------
# Local Run
# --------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
