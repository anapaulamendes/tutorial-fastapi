import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from db.application_dal import ApplicationDAL
from dependencies import get_application_dal

from serializers.user_serializer import UserSerializer

router = APIRouter()


@router.post("/users")
async def create_user(
    name: str,
    username: str,
    application_dal: ApplicationDAL = Depends(get_application_dal),
):
    try:
        user = await application_dal.create_user(name, username)
        user = UserSerializer(**user.__dict__).model_dump()
        user["id"] = str(user["id"])

        return JSONResponse(status_code=201, content=user)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/users", response_model=list[UserSerializer])
async def list_users(application_dal: ApplicationDAL = Depends(get_application_dal)):
    users = await application_dal.get_all_users()

    return users


@router.get("/users/{user_id}", response_model=UserSerializer)
async def get_user(
    user_id: uuid.UUID, application_dal: ApplicationDAL = Depends(get_application_dal)
):
    user = await application_dal.get_user(user_id=user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user
