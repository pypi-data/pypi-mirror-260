from fastapi import APIRouter, Depends

from komodo.loaders.user_loader import UserLoader
from komodo.server.globals import get_email_from_header

router = APIRouter(
    prefix='/api/v1/user',
    tags=['User']
)


@router.get("/profile", response_model=dict, summary="Get user profile.", description="Get user profile.")
async def get_user_profile(email: str = Depends(get_email_from_header)):
    user = UserLoader.load(email)
    return user.to_dict()
