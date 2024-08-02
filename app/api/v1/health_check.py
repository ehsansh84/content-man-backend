from fastapi import APIRouter, status, HTTPException
from publics import Settings

module_name = 'health_check'
module_text = 'HealthCheck'
router = APIRouter(
    prefix=f"/{module_name}",
    tags=[module_name]
)


@router.head("/", status_code=status.HTTP_200_OK)
@router.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    import pymongo
    client = pymongo.MongoClient(Settings.MONGO_URL)
    try:
        client.admin.command('ping')
        return "Operation successful"
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while checking MongoDB connection: {str(e)}")

