from pydantic import BaseModel
from typing import List

class SearchItem(BaseModel):
    id: int
    type: str
    title: str
    overview: str
    rating: float
    release_date: str | None
    poster: str | None

class SearchResponse(BaseModel):
    success: bool
    query: str
    total_results: int
    results: List[SearchItem]