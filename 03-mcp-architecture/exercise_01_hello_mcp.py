"""
Exercise 01: Hello MCP - 첫 번째 MCP 서버
FastMCP를 사용하여 간단한 echo 도구를 가진 MCP 서버를 만듭니다.

요구사항:
1. echo 도구: 메시지를 받아 "Echo: {message}" 형태로 반환
2. greet 도구: 이름을 받아 인사 메시지 반환

실행: python exercise_01_hello_mcp.py
"""
from fastmcp import FastMCP

mcp = FastMCP("Hello MCP")

# TODO: echo 도구를 구현하세요
# - @mcp.tool() 데코레이터 사용
# - message: str 파라미터
# - "Echo: {message}" 형태로 반환

# TODO: greet 도구를 구현하세요
# - @mcp.tool() 데코레이터 사용
# - name: str 파라미터
# - 인사 메시지 반환


if __name__ == "__main__":
    mcp.run()
