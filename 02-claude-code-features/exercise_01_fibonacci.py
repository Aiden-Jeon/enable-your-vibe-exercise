"""
Exercise 01: Fibonacci - Python 함수 만들기
Claude Code를 사용하여 fibonacci 수열 함수를 구현합니다.

요구사항:
1. fibonacci 함수: n개의 fibonacci 수를 리스트로 반환
2. 타입 힌트와 docstring 포함
3. n이 음수이면 ValueError 발생
4. n이 0이면 빈 리스트 반환

실행: python exercise_01_fibonacci.py
"""


def fibonacci(n: int) -> list[int]:
    """Generate fibonacci sequence.

    Args:
        n: Number of fibonacci numbers to generate.

    Returns:
        List of n fibonacci numbers.

    Raises:
        ValueError: If n is negative.
    """
    # TODO: fibonacci 함수를 구현하세요
    # - n이 음수이면 ValueError를 발생시킵니다
    # - n이 0이면 빈 리스트를 반환합니다
    # - n이 1이면 [0]을 반환합니다
    # - n이 2 이상이면 [0, 1, ...]로 n개의 fibonacci 수를 반환합니다
    raise NotImplementedError("TODO: Claude Code에게 구현을 요청하세요!")


if __name__ == "__main__":
    # 구현 후 아래 코드로 동작을 확인할 수 있습니다
    print(f"fibonacci(0)  = {fibonacci(0)}")
    print(f"fibonacci(1)  = {fibonacci(1)}")
    print(f"fibonacci(5)  = {fibonacci(5)}")
    print(f"fibonacci(10) = {fibonacci(10)}")
