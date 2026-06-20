from fastapi import APIRouter, HTTPException
from app.models.favorites import FavoriteItem
from app.core.database import favorites_collection
from app.core.logger import logger

from fastapi import APIRouter, HTTPException, status
from app.core.database import db  # Adjust this import to match your database module
from app.core.logger import logger

router = APIRouter()

@router.post("/favorites")
async def save_to_favorites(item: FavoriteItem):
    try:
        # Convert Pydantic object to native dictionary structure
        favorite_data = item.model_dump()
        
        # Use upsert configuration matching type & id composite keys to prevent duplications
        favorites_collection.update_one(
            {"id": item.id, "type": item.type},
            {"$set": favorite_data},
            upsert=True
        )
        logger.info(f"Successfully modified MongoDB favorited index: {item.title} ({item.type})")
        return {"success": True, "message": f"'{item.title}' processed into storage."}
    except Exception as e:
        logger.exception(f"MongoDB persistence fault handling registration pipeline: {str(e)}")
        raise HTTPException(status_code=500, detail="Database registration operation anomaly discovered.")

@router.get("/favorites")
async def get_all_favorites():
    try:
        # Retrieve all items from collection matching query constraint
        cursor = favorites_collection.find({}, {"_id": 0})  # Omit default MongoDB ObjectId field
        favorites_list = list(cursor)
        
        return {
            "success": True,
            "total_results": len(favorites_list),
            "results": favorites_list
        }
    except Exception as e:
        logger.exception(f"Retrieval extraction processing pipeline encountered error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database data lookup failure anomaly.")
    



@router.delete("/favorites/{media_type}/{item_id}")
async def delete_favorite(media_type: str, item_id: int):
    """
    Removes a movie or tv show item from the MongoDB cluster.
    If the document doesn't exist, it handles it gracefully.
    """
    if media_type not in ["movie", "tv"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid media type. Must be 'movie' or 'tv'."
        )

    logger.info(f"Received request to remove favorite: type={media_type}, id={item_id}")

    try:
        # Match documents by both their numeric id and specific media type
        result = db.favorites.delete_one({"id": item_id, "type": media_type})
        
        if result.deleted_count == 0:
            logger.warning(f"Favorite not found for deletion: type={media_type}, id={item_id}")
            # Instead of a hard crash, reply with a clear 404 response
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The requested item could not be found in your favorites collection."
            )
            
        logger.info(f"Successfully deleted favorite index from MongoDB: type={media_type}, id={item_id}")
        return {"success": True, "message": "Item successfully removed from favorites."}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Database error encountered during delete operation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal database anomaly prevented item removal."
        )    