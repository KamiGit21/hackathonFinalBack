from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class TestCase(BaseModel):
    input: str
    expected_output: str
    weight: Optional[float] = 1.0

class ExecutionRequest(BaseModel):
    submission_id: int
    language: str = Field(..., description="python, java, javascript")
    code: str
    tests: List[TestCase]

class TestResult(BaseModel):
    passed: bool
    input: str
    expected_output: str
    actual_output: str
    error: Optional[str] = None
    execution_time: Optional[float] = None

class ExecutionResponse(BaseModel):
    status: str  # OK, ERROR, TIMEOUT
    score: float
    details: Dict[str, Any]
    test_results: List[TestResult]
    total_tests: int
    passed_tests: int
    execution_time: float
    timestamp: datetime

class ExecutionLog(BaseModel):
    submission_id: int
    language: str
    status: str
    score: float
    execution_time: float
    output: str
    error: Optional[str] = None
    timestamp: datetime