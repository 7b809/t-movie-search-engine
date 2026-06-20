from fastapi import APIRouter, HTTPException

from app.models.request import SearchRequest
from app.services.tmdb_service import (
    search_movie,
    search_tv,
    map_result,
)
from app.core.logger import logger

router = APIRouter()


@router.post("/search")
async def search(request: SearchRequest):

    try:

        logger.info(
            f"Search request received | "
            f"query='{request.query}' | "
            f"type='{request.search_type}' | "
            f"page={request.page}"
        )

        results = []

        search_type = request.search_type.lower().strip()

        if search_type not in ["movie", "tv", "all"]:
            logger.warning(f"Invalid search_type received: {search_type}")

            raise HTTPException(
                status_code=400, detail="search_type must be movie, tv, or all"
            )

        if search_type == "movie":

            movie_data = await search_movie(
                request.query,
                request.page,
            )

            results.extend(
                [map_result(x, "movie") for x in movie_data.get("results", [])]
            )

        elif search_type == "tv":

            tv_data = await search_tv(
                request.query,
                request.page,
            )

            results.extend([map_result(x, "tv") for x in tv_data.get("results", [])])

        else:

            movie_data = await search_movie(
                request.query,
                request.page,
            )

            tv_data = await search_tv(
                request.query,
                request.page,
            )

            results.extend(
                [map_result(x, "movie") for x in movie_data.get("results", [])]
            )

            results.extend([map_result(x, "tv") for x in tv_data.get("results", [])])

        logger.info(
            f"Search completed | "
            f"query='{request.query}' | "
            f"results={len(results)}"
        )

        return {
            "success": True,
            "message": "Search completed successfully",
            "query": request.query,
            "search_type": search_type,
            "page": request.page,
            "total_results": len(results),
            "results": results,
        }

    except HTTPException:
        raise

    except Exception as e:

        logger.exception(
            f"Search failed | " f"query='{request.query}' | " f"error={str(e)}"
        )

        raise HTTPException(status_code=500, detail="Internal server error")
