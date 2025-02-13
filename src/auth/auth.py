from loguru import logger
from data.schemas import UserSchema
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Response, status, Depends
from database.core import get_db, AsyncSession, UserRepository
from auth.utils import get_password_hash, authenticate_user, create_access_token


logger.add('src/logs/auth.log', format="{time} {level} {message}\n", rotation='500MB', level="INFO", enqueue=True)
router = APIRouter()


@router.post("/register")
async def register_user(user_data: UserSchema, session: AsyncSession = Depends(get_db)):
    try:
        user = await UserRepository.get_user_from_db(user_data.username, session)
        if user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='User already exists')
        await UserRepository.register_user(user_data.username, get_password_hash(user_data.password), session)
        logger.info(f'Зарегистрирован пользователь: {user_data.username}')
        return {'message': 'You have successfully registered!'}
    except Exception as e:
        logger.error(f'Ошибка регистрации\n{str(e)}')


@router.post("/login")
async def auth_user(response: Response, user_data: UserSchema, session: AsyncSession = Depends(get_db)):
    try:
        user = await UserRepository.get_user_from_db(user_data.username, session)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="User doesn't exists")
        
        check = await authenticate_user(password=user_data.password, hashed_password=user.password, session=session)
        if not check:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Wrong password or username')
        access_token = create_access_token({"sub": str(user.username)})
        response.set_cookie(key="users_access_token", value=access_token, httponly=True)
        logger.info(f'Вошел пользователь: {user_data.username}')
        return {'message': 'You have successfully logged in!'}
    except Exception as e:
        logger.error(f'Ошибка входа\n{str(e)}')


@router.post("/logout/")
async def logout_user(response: Response):
    try:
        response.delete_cookie(key="users_access_token")
        return {'message': 'The user has successfully logged out'}
    except Exception as e:
        logger.error(f'Ошибка выхода:\n{str(e)}')