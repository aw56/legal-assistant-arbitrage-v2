from sqlalchemy import Column, Integer, String, Text

from backend.app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="client")


class Law(Base):
    __tablename__ = "laws"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)
    article = Column(String, nullable=False)
    title = Column(String, nullable=False)


class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True, index=True)
    case_number = Column(String, unique=True, index=True, nullable=False)
    court = Column(String, nullable=False)
    summary = Column(Text, nullable=True)
