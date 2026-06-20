from pydantic import BaseModel
from typing import Optional

class FavoriteItem(BaseModel):
    id: int
    type: str
    title: str
    overview: Optional[str] = None
    rating: float
    release_date: Optional[str] = None
    poster: Optional[str] = None