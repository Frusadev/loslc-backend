from sqlmodel import Session, SQLModel, create_engine

from app.env import DB_STRING

engine = create_engine(f"{DB_STRING}")


def setup_db():
    SQLModel.metadata.create_all(engine)


def generate_database_session():
    with Session(engine) as session:
        yield session
