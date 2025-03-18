import uuid
from datetime import datetime, timedelta
from typing import List

import sqlalchemy as sa
from sqlmodel import Field, Relationship, SQLModel, String

from app.utils.crypto import gen_id


class EventUserLink(SQLModel, table=True):
    event_id: uuid.UUID = Field(foreign_key="event.id", primary_key=True)
    user_email: str = Field(foreign_key="user.email", primary_key=True)


class User(SQLModel, table=True):
    email: str = Field(primary_key=True)
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    username: str
    account_type: str = Field(default="user")
    session_token: "AuthSession" = Relationship(back_populates="user")
    login_session: "LoginSession" = Relationship(back_populates="user")
    surveys: List["Survey"] = Relationship(back_populates="author")
    survey_questions: List["SurveyQuestion"] = Relationship(back_populates="author")
    survey_responses: List["SurveyResponse"] = Relationship(back_populates="responder")
    events_created: List["Event"] = Relationship(back_populates="author")
    events: List["Event"] = Relationship(
        back_populates="participants", link_model=EventUserLink
    )


class AuthSession(SQLModel, table=True):
    id: str = Field(default_factory=gen_id, primary_key=True)
    user_email: str = Field(foreign_key="user.email")
    user: User = Relationship(back_populates="session_token")
    expires_at: datetime = Field(
        default_factory=lambda: datetime.now() + timedelta(days=30)
    )


class LoginSession(SQLModel, table=True):
    id: str = Field(default_factory=gen_id, primary_key=True)
    user_email: str = Field(foreign_key="user.email")
    user: User = Relationship(back_populates="login_session")
    expires_at: datetime = Field(
        default_factory=lambda: datetime.now() + timedelta(hours=1)
    )


class Survey(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    author_email: str = Field(foreign_key="user.email")
    title: str
    description: str
    active: bool = Field(default=False)
    questions: list["SurveyQuestion"] = Relationship(back_populates="survey")
    responses: list["SurveyResponse"] = Relationship(back_populates="survey")
    author: User = Relationship(back_populates="surveys")


class SurveyQuestion(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    survey_id: uuid.UUID = Field(foreign_key="survey.id")
    survey: Survey = Relationship(back_populates="questions")
    author_email: str = Field(foreign_key="user.email")
    question_type: str = Field(default="select")  # select, mutliselect, text
    title: str
    responses: list["SurveyResponse"] = Relationship(back_populates="question")
    author: User = Relationship(back_populates="survey_questions")


class SurveyResponse(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    responder_email: str = Field(foreign_key="user.email")
    question_id: uuid.UUID = Field(foreign_key="surveyquestion.id", unique=True)
    survey_id: uuid.UUID = Field(foreign_key="survey.id")
    survey: Survey = Relationship(back_populates="responses")
    question: SurveyQuestion = Relationship(back_populates="responses")
    values: List[str] = Field(sa_column=sa.Column(sa.ARRAY(String)))
    responder: User = Relationship(back_populates="survey_responses")


class Event(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    description: str
    date: datetime
    location: str
    cover_image_url: str
    author_email: str = Field(foreign_key="user.email")
    author: User = Relationship(back_populates="events_created")
    participants: List["User"] = Relationship(
        back_populates="events", link_model=EventUserLink
    )
