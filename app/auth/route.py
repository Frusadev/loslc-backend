from typing import Annotated

from fastapi import APIRouter, Depends, Form
from pydantic import EmailStr
from sqlmodel import Session

from app.auth.auth_service import login_user, register_user, verify_login_token
from app.db.database import generate_database_session
from app.env import FRONTEND_URL

auth_router = APIRouter()


@auth_router.post("/auth/register")
async def register(
    db_session: Annotated[Session, Depends(generate_database_session)],
    username: str = Form(),
    email: EmailStr = Form(),
):
    return register_user(username=username, email=email, db_session=db_session)


@auth_router.post("/auth/login")
async def login(
    db_session: Annotated[Session, Depends(generate_database_session)],
    email: EmailStr = Form(),
):
    return login_user(email=email, db_session=db_session)


@auth_router.get("/auth/token")
async def verify_token(
    token: str,
    db_session: Annotated[Session, Depends(generate_database_session)],
    from_url: str = f"{FRONTEND_URL}/v1/auth/login",
):
    return verify_login_token(token=token, db_session=db_session, from_url=from_url)
