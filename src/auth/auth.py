
from sqlalchemy import select
from database.models import User
from data.schemas import UserSchema
from fastapi.exceptions import HTTPException
from database.core import get_db, AsyncSession
from fastapi import APIRouter, Response, status, Depends
from auth.utils import get_password_hash, authenticate_user, create_access_token


router = APIRouter()


@router.post("/register")
async def register_user(user_data: UserSchema, session: AsyncSession = Depends(get_db)) -> dict:
    user = (await session.execute(select(User).where(User.username == user_data.username))).scalar_one_or_none()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='User already exists')
    session.add(User(username = user_data.username, password = get_password_hash(user_data.password)))
    await session.commit()
    return {'message': 'You have successfully registered!'}


@router.post("/login")
async def auth_user(response: Response, user_data: UserSchema, session: AsyncSession = Depends(get_db)):
    check = await authenticate_user(username=user_data.username, password=user_data.password, session=session)
    if not check:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Wrong password or username')
    access_token = create_access_token({"sub": str(check.username)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'message': 'You have successfully logged in!'}


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'The user has successfully logged out'}
