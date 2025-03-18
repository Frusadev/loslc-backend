from pydantic import BaseModel

from app.db.models import User


class UserSchema(BaseModel):
    username: str
    email: str
    account_type: str

    @classmethod
    def from_model(cls, user: User):
        return cls(
            username=user.username,
            email=user.email,
            account_type=user.account_type,
        )

    def to_model(self):
        return User(
            username=self.username,
            email=self.email,
            account_type=self.account_type,
        )
