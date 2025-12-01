from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.db import Base


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    attempt_number = Column(Integer, nullable=False, default=1)

    code = Column(String, nullable=False)  # simplificado, podrías usar Text
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    status = Column(String(20), nullable=False, default="PENDING")
    # Ej: "PENDING", "EXECUTED", "GRADED", "REJECTED_DEADLINE"

    score = Column(Float, nullable=True)  # nota de este intento

    # Relación para facilitar queries
    assignment = relationship("Assignment", backref="submissions")
    # user relationship si quieres, opcional

