from logging import getLogger

from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.configs.session import get_db
from app.exception_handlers import InvalidData
from app.models.db_models import User
from app.models.validatable_models import UserResponse, UserCreate

users_api_router = APIRouter(prefix="/api", tags=["api"])
api_logger = getLogger('api')


@users_api_router.post("/user/",
                       summary="Create a new user.",
                       status_code=status.HTTP_201_CREATED,
                       response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the database using the provided user data.

    This endpoint will attempt to add a new user to the database based on the data provided in the `user` parameter.
    It handles database sessions and commits internally. If the data violates database integrity, an `InvalidData`
    exception is raised.

    Args:
        user (UserCreate): The user data to be created. This should be a validated instance of UserCreate.
        db (Session): The database session dependency, typically injected by FastAPI's dependency injection system.

    Returns:
        dict: A dictionary representation of the created user, typically conforming to the UserResponse model.

    Raises:
        InvalidData: If the data provided violates database integrity constraints, this exception is raised,
                     indicating that the input data is invalid.
    """
    user_instance = User(**user.model_dump())

    db.add(user_instance)
    try:
        db.commit()
        db.refresh(user_instance)
    except IntegrityError:
        api_logger.exception('Error adding new user')
        raise InvalidData()
    api_logger.debug('Created new user')
    return user_instance.__dict__
