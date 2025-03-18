from datetime import datetime
from typing import Annotated

from fastapi import Cookie, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import EmailStr
from sqlmodel import Session

from app.db.database import generate_database_session
from app.db.models import AuthSession, LoginSession, User
from app.env import SERVER_URL
from app.services.email import send_email

def register_user(username: str, email: EmailStr, db_session: Session):
    user = User(email=email, username=username)
    db_session.add(user)
    db_session.commit()
    response = JSONResponse(
        content={
            "message": "You were successfully registered",
            "login_url": f"{SERVER_URL}/v1/auth/login",
        }
    )
    response.status_code = 201
    return response


def login_user(email: EmailStr, db_session: Session):
    user = db_session.get(User, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    login_session = LoginSession(user_email=user.email)
    db_session.add(login_session)
    db_session.commit()
    db_session.refresh(login_session)
    send_email(
        email=email,
        subject="Linux and open-source lovers community login link",
        message=f"{SERVER_URL}/v1/auth/token?token={login_session.id}",
    )
    response = JSONResponse(
        content={
            "message": "Login link sent to client email address",
        }
    )
    response.status_code = 200
    return response


def verify_login_token(
    token: str,
    db_session: Session,
    from_url: str,
):
    login_session = db_session.get(LoginSession, token)
    if not login_session:
        raise HTTPException(status_code=404, detail="Token not found")
    if login_session.expires_at < datetime.now():
        db_session.delete(login_session)
        db_session.commit()
        raise HTTPException(status_code=401, detail="Token expired")
    user = login_session.user
    if not user:
        raise HTTPException(status_code=401, detail="Invalid login session")

    auth_session = AuthSession(user_email=user.email)
    db_session.add(auth_session)
    db_session.commit()
    db_session.refresh(auth_session)
    response = JSONResponse(content={"redirect": from_url}, status_code=200)
    response.set_cookie(key="session", value=auth_session.id, httponly=True)
    return response


def get_current_user(
    db_session: Annotated[Session, Depends(generate_database_session)],
    session: Annotated[str | None, Cookie()] = None,
):
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")
    auth_session = db_session.get(AuthSession, session)
    if not auth_session:
        raise HTTPException(status_code=401, detail="Invalid session")
    if auth_session.expires_at < datetime.now():
        db_session.delete(auth_session)
        db_session.commit()
        raise HTTPException(status_code=401, detail="Session expired")
    user = auth_session.user
    if not user:
        raise HTTPException(status_code=401, detail="Invalid session")
    return user
