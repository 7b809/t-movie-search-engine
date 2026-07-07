from fastapi import APIRouter, HTTPException, status
from app.models.favorites import FavoriteItem
from app.core.database import daily_watch_collection, db
from app.core.logger import logger

router = APIRouter()


@router.post("/daily-watch")
async def save_to_daily_watch(item: FavoriteItem):
    try:
        favorite_data = item.model_dump()
        daily_watch_collection.update_one(
            {"id": item.id, "type": item.type}, {"$set": favorite_data}, upsert=True
        )
        return {"success": True, "message": f"'{item.title}' added to Daily Watch."}
    except Exception as e:
        logger.exception(f"Daily Watch persistence error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database operation failed.")


@router.get("/daily-watch")
async def get_all_daily_watch():
    try:
        cursor = daily_watch_collection.find({}, {"_id": 0})
        return {"success": True, "results": list(cursor)}
    except Exception as e:
        logger.exception(f"Daily Watch retrieval error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database lookup failed.")


@router.delete("/daily-watch/{media_type}/{item_id}")
async def delete_daily_watch(media_type: str, item_id: int):
    result = db.daily_watch.delete_one({"id": item_id, "type": media_type})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found.")
    return {"success": True, "message": "Removed from Daily Watch."}
