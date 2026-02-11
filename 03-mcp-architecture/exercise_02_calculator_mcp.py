"""
Exercise 02: Calculator MCP - 계산기 MCP 서버
사칙연산을 수행하는 MCP 서버를 만듭니다.

실행: python exercise_02_calculator_mcp.py
"""
from fastmcp import FastMCP

mcp = FastMCP("Calculator")


@mcp.tool()
def add(a: float, b: float) -> float:
    """두 수를 더합니다."""
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """두 수를 뺍니다."""
    return a - b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """두 수를 곱합니다."""
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """두 수를 나눕니다."""
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다.")
    return a / b


if __name__ == "__main__":
    mcp.run()
