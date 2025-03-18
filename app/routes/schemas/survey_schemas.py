import uuid

from pydantic import BaseModel, field_validator

from app.db.models import Survey, SurveyQuestion, SurveyResponse
from app.routes.schemas.user_schemas import UserSchema


class SurveySchema(BaseModel):
    id: str | None = None
    title: str
    description: str
    active: bool
    author: UserSchema

    @classmethod
    def from_model(cls, survey: Survey):
        return cls(
            id=str(survey.id),
            title=survey.title,
            description=survey.description,
            active=survey.active,
            author=UserSchema.from_model(survey.author),
        )

    def to_model(self):
        return Survey(
            id=uuid.UUID(self.id),
            title=self.title,
            description=self.description,
            active=self.active,
            author_email=self.author.email,
        )


class SurveyQuestionSchema(BaseModel):
    id: str | None = None
    author: UserSchema
    survey_id: uuid.UUID
    title: str
    question_type: str

    @classmethod
    def from_model(cls, question: SurveyQuestion):
        return cls(
            id=str(question.id),
            survey_id=question.survey_id,
            title=question.title,
            author=UserSchema.from_model(question.author),
            question_type=question.question_type,
        )

    def to_model(self):
        return SurveyQuestion(
            id=uuid.UUID(self.id),
            survey_id=self.survey_id,
            title=self.title,
            question_type=self.question_type,
            author_email=self.author.email,
        )


class SurveyResponseSchema(BaseModel):
    id: uuid.UUID | None = None
    survey_id: uuid.UUID
    question_id: uuid.UUID
    answers: list[str]
    response_type: str  # select, mutliselect, tex
    responder_email: str

    @classmethod
    def from_model(cls, response: SurveyResponse):
        return cls(
            id=response.id,
            survey_id=response.survey_id,
            question_id=response.question_id,
            answers=response.values,
            response_type=response.question.question_type,
            responder_email=response.responder_email,
        )

    @field_validator("answers")
    def validate_answers(cls, answers: list[str]):
        match cls.response_type:
            case "select":
                if len(answers) != 1:
                    raise ValueError("Only one answer is allowed")
            case "multiselect":
                if len(answers) < 1:
                    raise ValueError("At least one answer is required")
            case "text":
                if len(answers) != 1:
                    raise ValueError("Only one answer is allowed")

    def to_model(self):
        return SurveyResponse(
            id=self.id if self.id else uuid.uuid4(),
            survey_id=self.survey_id,
            question_id=self.question_id,
            values=self.answers,
            responder_email=self.responder_email,
        )
