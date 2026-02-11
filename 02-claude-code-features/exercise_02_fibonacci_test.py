"""
Exercise 02: Fibonacci 테스트 - pytest 테스트 작성
Claude Code를 사용하여 fibonacci 함수의 테스트를 구현합니다.

요구사항:
1. 기본 동작 테스트 (fibonacci(5) 결과 확인)
2. Edge case 테스트 (0, 1, 음수)
3. 큰 수 테스트 (fibonacci(10))

실행: uv run --with pytest pytest exercise_02_fibonacci_test.py -v
"""

import pytest

from exercise_01_fibonacci import fibonacci


# TODO: 기본 동작 테스트를 구현하세요
# - fibonacci(5)가 [0, 1, 1, 2, 3]을 반환하는지 확인
def test_fibonacci_basic():
    raise NotImplementedError("TODO: Claude Code에게 구현을 요청하세요!")


# TODO: n=0 테스트를 구현하세요
# - fibonacci(0)이 빈 리스트를 반환하는지 확인
def test_fibonacci_zero():
    raise NotImplementedError("TODO: Claude Code에게 구현을 요청하세요!")


# TODO: n=1 테스트를 구현하세요
# - fibonacci(1)이 [0]을 반환하는지 확인
def test_fibonacci_one():
    raise NotImplementedError("TODO: Claude Code에게 구현을 요청하세요!")


# TODO: 음수 입력 테스트를 구현하세요
# - fibonacci(-1) 호출 시 ValueError가 발생하는지 확인
# - pytest.raises를 사용하세요
def test_fibonacci_negative():
    raise NotImplementedError("TODO: Claude Code에게 구현을 요청하세요!")


# TODO: 큰 수 테스트를 구현하세요
# - fibonacci(10)의 길이가 10인지 확인
# - 마지막 값이 34인지 확인
def test_fibonacci_large():
    raise NotImplementedError("TODO: Claude Code에게 구현을 요청하세요!")
