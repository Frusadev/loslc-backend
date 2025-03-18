from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.auth.auth_service import get_current_user
from app.db.database import generate_database_session
from app.db.models import User
from app.routes.schemas.survey_schemas import (
    SurveyQuestionSchema,
    SurveyResponseSchema,
    SurveySchema,
)
from app.routes.services.survey_service import (
    add_survey,
    add_survey_question,
    add_survey_response,
    change_survey_response,
    delete_survey,
    delete_survey_question,
    delete_survey_response,
    get_all_active_surveys,
    get_all_surveys,
    get_survey,
    get_survey_questions,
    get_survey_response,
    get_survey_responses,
    update_survey,
    update_survey_question,
)

survey_router = APIRouter()


@survey_router.get("/surveys")
async def get_surveys(
    user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(generate_database_session)],
    offset: int = 0,
    limit: int = Query(default=10, le=10),
    active: bool = True,
):
    if active:
        return get_all_active_surveys(
            offset=offset, limit=limit, user=user, db_session=db_session
        )
    return get_all_surveys(offset=offset, limit=limit, user=user, db_session=db_session)


@survey_router.get("/surveys/{survey_id}")
async def gt_survey(
    survey_id: str,
    user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(generate_database_session)],
):
    return get_survey(UUID(survey_id), db_session=db_session, user=user)


@survey_router.post("/survey/create", status_code=201)
async def create_survey(
    survey: SurveySchema,
    user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(generate_database_session)],
):
    return add_survey(survey, user=user, db_session=db_session)


@survey_router.put("/survey/edit", status_code=201)
async def upd_survey(
    survey: SurveySchema,
    user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(generate_database_session)],
):
    return update_survey(survey, user=user, db_session=db_session)


@survey_router.delete("/surveys/delete/{survey_id}", status_code=204)
async def del_survey(
    survey_id: str,
    user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(generate_database_session)],
):
    return delete_survey(UUID(survey_id), user=user, db_session=db_session)


@survey_router.get("/surveys/{survey_id}/questions")
async def gt_survey_questions(
    survey_id: str,
    user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(generate_database_session)],
):
    return get_survey_questions(UUID(survey_id), user=user, db_session=db_session)


@survey_router.post("/surveys/{survey_id}/questions/create", status_code=201)
async def create_survey_question(
    survey_id: str,
    question: SurveyQuestionSchema,
    user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(generate_database_session)],
):
    return add_survey_question(
        survey_id=UUID(survey_id), question=question, user=user, db_session=db_session
    )


@survey_router.put("/survey/questions/edit", status_code=201)
async def upd_survey_question(
    question: SurveyQuestionSchema,
    user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(generate_database_session)],
):
    return update_survey_question(question, user=user, db_session=db_session)


@survey_router.delete("/survey/questions/delete", status_code=204)
async def del_survey_question(
    question_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(generate_database_session)],
):
    return delete_survey_question(question_id, user=user, db_session=db_session)


@survey_router.get("/survey/response/{response_id}")
async def gt_survey_response(
    response_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(generate_database_session)],
):
    return get_survey_response(
        user=user, db_session=db_session, response_id=response_id
    )


@survey_router.get("/surveys/{survey_id}/responses")
async def gt_survey_responses(
    survey_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(generate_database_session)],
    offset: int = 0,
    limit: int = Query(default=10, le=10),
):
    return get_survey_responses(
        survey_id=survey_id,
        user=user,
        db_session=db_session,
        offset=offset,
        limit=limit,
    )


@survey_router.post("/surveys/{survey_id}/response", status_code=201)
async def create_survey_response(
    survey_id: UUID,
    question_id: UUID,
    survey_response: SurveyResponseSchema,
    user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(generate_database_session)],
):
    return add_survey_response(
        survey_id=survey_id,
        response=survey_response,
        user=user,
        db_session=db_session,
        question_id=question_id,
    )


@survey_router.put("/survey/response/edit", status_code=201)
async def upd_survey_response(
    survey_id: UUID,
    question_id: UUID,
    response: SurveyResponseSchema,
    user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(generate_database_session)],
):
    return change_survey_response(
        survey_id=survey_id,
        question_id=question_id,
        response=response,
        user=user,
        db_session=db_session,
    )


@survey_router.delete("/survey/response/{response_id}/delete", status_code=204)
async def del_survey_response(
    response_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(generate_database_session)],
):
    return delete_survey_response(
        user=user, db_session=db_session, response_id=response_id
    )
