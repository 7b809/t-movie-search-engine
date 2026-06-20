from pydantic import BaseModel

class SearchRequest(BaseModel):
    query: str
    search_type: str = "all"
    page: int = 1