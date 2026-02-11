#!/bin/bash
# Databricks endpoint 설정을 클립보드에서 .claude/settings.local.json으로 적용

set -e

TARGET_DIR=".claude"
TARGET_FILE="$TARGET_DIR/settings.local.json"

# 1. 클립보드 읽기
CLIPBOARD=$(pbpaste 2>/dev/null)
if [ -z "$CLIPBOARD" ]; then
    echo "❌ 클립보드가 비어있습니다. 설정 JSON을 먼저 복사해주세요."
    exit 1
fi

# 2. JSON 유효성 검증
if ! echo "$CLIPBOARD" | python3 -c "import sys, json; json.load(sys.stdin)" 2>/dev/null; then
    echo "❌ 클립보드 내용이 유효한 JSON이 아닙니다."
    exit 1
fi

# 3. 디렉토리 생성
mkdir -p "$TARGET_DIR"

# 4. 기존 파일 백업
if [ -f "$TARGET_FILE" ]; then
    cp "$TARGET_FILE" "${TARGET_FILE}.bak"
    echo "📋 기존 설정 백업: ${TARGET_FILE}.bak"
fi

# 5. 파일 쓰기
echo "$CLIPBOARD" > "$TARGET_FILE"
echo "✅ 설정 완료: $TARGET_FILE"
