"""
Exercise 01: Hello MCP - 첫 번째 MCP 서버
FastMCP를 사용하여 간단한 echo 도구를 가진 MCP 서버를 만듭니다.

실행: python exercise_01_hello_mcp.py
"""
from fastmcp import FastMCP

mcp = FastMCP("Hello MCP")


@mcp.tool()
def echo(message: str) -> str:
    """메시지를 그대로 반환합니다."""
    return f"Echo: {message}"


@mcp.tool()
def greet(name: str) -> str:
    """이름을 받아 인사합니다."""
    return f"안녕하세요, {name}님! 👋"


if __name__ == "__main__":
    mcp.run()
