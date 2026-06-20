import httpx

from app.core.config import (
    TMDB_API_KEY,
    TMDB_BASE_URL,
    POSTER_BASE_URL
)

client = httpx.AsyncClient()


async def search_movie(
        query: str,
        page: int):

    url = (
        f"{TMDB_BASE_URL}/search/movie"
    )

    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "page": page
    }

    response = await client.get(
        url,
        params=params
    )

    return response.json()

async def search_tv(
        query: str,
        page: int):

    url = (
        f"{TMDB_BASE_URL}/search/tv"
    )

    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "page": page
    }

    response = await client.get(
        url,
        params=params
    )

    return response.json()


def map_result(
    item,
    media_type
):

    return {
        "id": item["id"],
        "type": media_type,
        "title":
            item.get("title")
            or item.get("name"),
        "overview":
            item.get("overview"),
        "rating":
            item.get(
                "vote_average",
                0
            ),
        "release_date":
            item.get(
                "release_date"
            )
            or item.get(
                "first_air_date"
            ),
        "poster":
            (
                f"{POSTER_BASE_URL}"
                f"{item['poster_path']}"
            )
            if item.get(
                "poster_path"
            )
            else None
    }