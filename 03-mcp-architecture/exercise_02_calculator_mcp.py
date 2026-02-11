"""
Exercise 02: Calculator MCP - 계산기 MCP 서버
사칙연산을 수행하는 MCP 서버를 만듭니다.

요구사항:
1. add: 두 수를 더합니다
2. subtract: 두 수를 뺍니다
3. multiply: 두 수를 곱합니다
4. divide: 두 수를 나눕니다 (0으로 나누기 에러 처리)

실행: python exercise_02_calculator_mcp.py
"""
from fastmcp import FastMCP

mcp = FastMCP("Calculator")

# TODO: 사칙연산 도구 4개를 구현하세요
# - @mcp.tool() 데코레이터 사용
# - 각 함수는 a: float, b: float 파라미터
# - divide는 0으로 나누기 에러 처리 포함


if __name__ == "__main__":
    mcp.run()
