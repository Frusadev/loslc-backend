from uuid import UUID

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session, select

from app.db.models import Survey, SurveyQuestion, SurveyResponse, User
from app.routes.schemas.survey_schemas import (
    SurveyQuestionSchema,
    SurveyResponseSchema,
    SurveySchema,
)


def get_all_active_surveys(
    offset: int,
    limit: int,
    user: User,
    db_session: Session,
):
    if not user.account_type == "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    stmt = select(Survey).where(Survey.active).offset(offset).limit(limit)
    active_surveys_in_db = db_session.exec(stmt)
    active_surveys = [
        SurveySchema.from_model(survey) for survey in active_surveys_in_db.all()
    ]
    return active_surveys


def get_all_surveys(
    offset: int,
    limit: int,
    user: User,
    db_session: Session,
):
    if not user.account_type == "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    stmt = select(Survey).offset(offset).limit(limit)
    surveys_in_db = db_session.exec(stmt)
    surveys = [SurveySchema.from_model(survey) for survey in surveys_in_db.all()]
    return surveys


def get_survey(id: UUID, db_session: Session, user: User):
    survey = db_session.get(Survey, id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    survey_response = SurveySchema.from_model(survey)
    return survey_response


def add_survey(
    survey: SurveySchema,
    db_session: Session,
    user: User,
):
    db_survey = Survey(
        author_email=user.email,
        title=survey.title,
        description=survey.description,
        active=survey.active,
    )
    db_session.add(db_survey)
    db_session.commit()
    db_session.refresh(db_survey)
    response = SurveySchema.from_model(db_survey)
    return response


def update_survey(
    survey: SurveySchema,
    db_session: Session,
    user: User,
):
    survey_in_db = db_session.get(Survey, UUID(survey.id))

    if not survey_in_db:
        raise HTTPException(status_code=404, detail="Survey not found")

    db_survey = Survey(
        id=UUID(survey.id),
        author_email=user.email,
        title=survey.title,
        description=survey.description,
        active=survey.active,
    )
    db_session.add(db_survey)
    db_session.commit()
    db_session.refresh(db_survey)
    return SurveySchema.from_model(db_survey)


def delete_survey(id: UUID, user: User, db_session: Session):
    if not user.account_type == "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    survey = db_session.get(Survey, id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    db_session.delete(survey)
    db_session.commit()
    return JSONResponse(
        content={"message": "Survey deleted successfully"}, status_code=200
    )


def add_survey_question(
    survey_id: UUID, question: SurveyQuestionSchema, user: User, db_session: Session
):
    if not user.account_type == "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    survey = db_session.get(Survey, survey_id)

    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    db_question: SurveyQuestion = question.to_model()
    db_question.survey_id = survey_id
    db_session.add(db_question)
    db_session.commit()
    db_session.refresh(db_question)
    return SurveyQuestionSchema.from_model(db_question)


def update_survey_question(
    question: SurveyQuestionSchema,
    user: User,
    db_session: Session,
):
    if not user.account_type == "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    if question.id is None:
        raise ValueError("Question ID is required")

    db_question = db_session.get(SurveyQuestion, UUID(question.id))
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    db_session.add(question.to_model())
    db_session.commit()
    return SurveyQuestionSchema.from_model(db_question)


def delete_survey_question(
    question_id: UUID,
    db_session: Session,
    user: User,
):
    if not user.account_type == "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    db_question = db_session.get(SurveyQuestion, question_id)
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    db_session.delete(db_question)
    db_session.commit()
    return JSONResponse(
        content={"message": "Question deleted successfully"}, status_code=200
    )


def get_survey_questions(
    survey_id: UUID,
    user: User,
    db_session: Session,
):
    survey = db_session.get(Survey, survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    questions = survey.questions
    response = [SurveyQuestionSchema.from_model(question) for question in questions]
    return response


def add_survey_response(
    survey_id: UUID,
    question_id: UUID,
    response: SurveyResponseSchema,
    user: User,
    db_session: Session,
):
    if not user.email == response.responder_email:
        raise HTTPException(status_code=403, detail="Forbidden")
    survey = db_session.get(Survey, survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    question = db_session.get(SurveyQuestion, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    db_response = response.to_model()
    db_session.add(db_response)
    db_session.commit()
    resp = SurveyResponseSchema.from_model(db_response)
    return resp


def change_survey_response(
    survey_id: UUID,
    question_id: UUID,
    response: SurveyResponseSchema,
    user: User,
    db_session: Session,
):
    if not response.id:
        raise HTTPException(status_code=404, detail="Response id must be provided")
    if not user.email == response.responder_email:
        raise HTTPException(status_code=403, detail="Forbidden")
    survey = db_session.get(Survey, survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    question = db_session.get(SurveyQuestion, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    db_response = db_session.get(SurveyResponse, response.id)
    if not db_response:
        raise HTTPException(status_code=404, detail="Response not found")
    db_session.add(db_response)
    db_session.commit()
    resp = SurveyResponseSchema.from_model(db_response)
    return resp


def delete_survey_response(user: User, db_session: Session, response_id: UUID):
    db_response = db_session.get(SurveyResponse, response_id)
    if not db_response:
        raise HTTPException(status_code=404, detail="Response not found")
    if not user.email == db_response.responder_email:
        raise HTTPException(status_code=403, detail="Forbidden")
    db_session.delete(db_session)
    db_session.commit()
    return JSONResponse(
        content={"message": "Response deleted successfully"}, status_code=200
    )


def get_survey_responses(
    user: User, db_session: Session, survey_id: UUID, offset: int, limit: int
):
    if not user.account_type == "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    db_survey = db_session.get(Survey, survey_id)
    if not db_survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    stmt = (
        select(SurveyResponse)
        .where(SurveyResponse.survey_id == survey_id)
        .offset(offset)
        .limit(limit)
    )
    responses = [
        SurveyResponseSchema.from_model(response)
        for response in db_session.exec(stmt).all()
    ]
    return responses


def get_survey_response(user: User, db_session: Session, response_id: UUID):
    db_response = db_session.get(SurveyResponse, response_id)
    if not db_response:
        raise HTTPException(status_code=404, detail="Response not found")
    if (
        not user.account_type == "admin"
        or not user.email == db_response.responder_email
    ):
        raise HTTPException(status_code=403, detail="Forbidden")
    response = SurveyResponseSchema.from_model(db_response)
    return response
