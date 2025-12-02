import subprocess
import tempfile
import os
import time
import logging
from typing import List, Dict, Any
from app.schemas import TestCase, TestResult, ExecutionResponse
from app.config import settings
from datetime import datetime

logger = logging.getLogger(__name__)

class ExecutionService:
    
    def __init__(self):
        self.timeout = settings.EXECUTION_TIMEOUT
        self.max_output_size = settings.MAX_OUTPUT_SIZE
    
    def execute_code(self, submission_id: int, language: str, code: str, tests: List[TestCase]) -> ExecutionResponse:
        """Ejecutar código y calificar con tests"""
        start_time = time.time()
        test_results = []
        passed_tests = 0
        
        try:
            # Validar lenguaje
            if language not in settings.ALLOWED_LANGUAGES:
                return ExecutionResponse(
                    status="ERROR",
                    score=0.0,
                    details={"error": f"Lenguaje no soportado: {language}"},
                    test_results=[],
                    total_tests=len(tests),
                    passed_tests=0,
                    execution_time=0.0,
                    timestamp=datetime.utcnow()
                )
            
            # Ejecutar cada test
            for test in tests:
                test_result = self._run_single_test(code, language, test)
                test_results.append(test_result)
                if test_result.passed:
                    passed_tests += 1
            
            # Calcular score
            total_tests = len(tests)
            score = (passed_tests / total_tests * 100) if total_tests > 0 else 0
            
            execution_time = time.time() - start_time
            
            return ExecutionResponse(
                status="OK",
                score=round(score, 2),
                details={
                    "message": f"Ejecutados {total_tests} tests",
                    "passed": passed_tests,
                    "failed": total_tests - passed_tests
                },
                test_results=test_results,
                total_tests=total_tests,
                passed_tests=passed_tests,
                execution_time=round(execution_time, 3),
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error ejecutando código: {e}")
            execution_time = time.time() - start_time
            return ExecutionResponse(
                status="ERROR",
                score=0.0,
                details={"error": str(e)},
                test_results=test_results,
                total_tests=len(tests),
                passed_tests=passed_tests,
                execution_time=round(execution_time, 3),
                timestamp=datetime.utcnow()
            )
    
    def _run_single_test(self, code: str, language: str, test: TestCase) -> TestResult:
        """Ejecutar un test individual"""
        test_start = time.time()
        
        try:
            if language == "python":
                return self._run_python_test(code, test, test_start)
            elif language == "java":
                return self._run_java_test(code, test, test_start)
            elif language == "javascript":
                return self._run_javascript_test(code, test, test_start)
            else:
                return TestResult(
                    passed=False,
                    input=test.input,
                    expected_output=test.expected_output,
                    actual_output="",
                    error=f"Lenguaje no implementado: {language}",
                    execution_time=0.0
                )
        except Exception as e:
            return TestResult(
                passed=False,
                input=test.input,
                expected_output=test.expected_output,
                actual_output="",
                error=str(e),
                execution_time=time.time() - test_start
            )
    
    def _run_python_test(self, code: str, test: TestCase, start_time: float) -> TestResult:
        """Ejecutar test en Python"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Ejecutar con subprocess
                result = subprocess.run(
                    ['python3', temp_file],
                    input=test.input,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout
                )
                
                actual_output = result.stdout.strip()
                expected_output = test.expected_output.strip()
                
                # Limitar tamaño de output
                if len(actual_output) > self.max_output_size:
                    actual_output = actual_output[:self.max_output_size] + "... (truncado)"
                
                passed = actual_output == expected_output
                error = result.stderr if result.stderr else None
                
                return TestResult(
                    passed=passed,
                    input=test.input,
                    expected_output=expected_output,
                    actual_output=actual_output,
                    error=error,
                    execution_time=round(time.time() - start_time, 3)
                )
                
            finally:
                # Limpiar archivo temporal
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                    
        except subprocess.TimeoutExpired:
            return TestResult(
                passed=False,
                input=test.input,
                expected_output=test.expected_output,
                actual_output="",
                error=f"Timeout: Ejecución excedió {self.timeout} segundos",
                execution_time=self.timeout
            )
        except Exception as e:
            return TestResult(
                passed=False,
                input=test.input,
                expected_output=test.expected_output,
                actual_output="",
                error=str(e),
                execution_time=round(time.time() - start_time, 3)
            )
    
    def _run_java_test(self, code: str, test: TestCase, start_time: float) -> TestResult:
        """Ejecutar test en Java (básico)"""
        # Implementación básica - expandir según necesidad
        return TestResult(
            passed=False,
            input=test.input,
            expected_output=test.expected_output,
            actual_output="",
            error="Java execution no implementado completamente",
            execution_time=0.0
        )
    
    def _run_javascript_test(self, code: str, test: TestCase, start_time: float) -> TestResult:
        """Ejecutar test en JavaScript (básico)"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                result = subprocess.run(
                    ['node', temp_file],
                    input=test.input,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout
                )
                
                actual_output = result.stdout.strip()
                expected_output = test.expected_output.strip()
                
                passed = actual_output == expected_output
                error = result.stderr if result.stderr else None
                
                return TestResult(
                    passed=passed,
                    input=test.input,
                    expected_output=expected_output,
                    actual_output=actual_output,
                    error=error,
                    execution_time=round(time.time() - start_time, 3)
                )
            finally:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                    
        except subprocess.TimeoutExpired:
            return TestResult(
                passed=False,
                input=test.input,
                expected_output=test.expected_output,
                actual_output="",
                error=f"Timeout: Ejecución excedió {self.timeout} segundos",
                execution_time=self.timeout
            )
        except Exception as e:
            return TestResult(
                passed=False,
                input=test.input,
                expected_output=test.expected_output,
                actual_output="",
                error=str(e),
                execution_time=round(time.time() - start_time, 3)
            )