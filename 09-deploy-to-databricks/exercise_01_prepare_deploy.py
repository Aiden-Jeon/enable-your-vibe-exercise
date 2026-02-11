"""
Exercise 01: 배포 준비
Databricks Apps 배포를 위한 app.yaml 생성 및 프로젝트 구조 확인

실행: python exercise_01_prepare_deploy.py
"""
import os
import yaml


def create_app_yaml(app_name: str = "genie-chatbot", port: int = 8000) -> dict:
    """Databricks Apps용 app.yaml을 생성합니다."""
    config = {
        "command": [
            "uvicorn",
            "app:app",
            "--host", "0.0.0.0",
            "--port", str(port),
        ],
        "env": [
            {"name": "DATABRICKS_HOST", "value": "{{DATABRICKS_HOST}}"},
            {"name": "DATABRICKS_TOKEN", "valueFrom": "secret"},
            {"name": "GENIE_SPACE_ID", "value": "{{GENIE_SPACE_ID}}"},
        ],
    }
    return config


def check_project_structure():
    """배포에 필요한 파일들이 있는지 확인합니다."""
    required_files = [
        "app.py",
        "static/index.html",
        "static/style.css",
        "static/app.js",
    ]

    print("📋 프로젝트 구조 확인")
    print("=" * 40)
    all_ok = True
    for f in required_files:
        exists = os.path.exists(f)
        status = "✅" if exists else "❌"
        print(f"  {status} {f}")
        if not exists:
            all_ok = False

    return all_ok


def main():
    print("🚀 Databricks Apps 배포 준비")
    print("=" * 50)

    # Step 1: app.yaml 생성
    print("\n1️⃣ app.yaml 생성")
    config = create_app_yaml()
    yaml_content = yaml.dump(config, default_flow_style=False, allow_unicode=True)
    print(f"\n{yaml_content}")

    # 파일로 저장
    with open("app.yaml", "w") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    print("   ✅ app.yaml 저장 완료")

    # Step 2: 배포 명령어 안내
    print("\n2️⃣ 배포 명령어")
    print("   # Databricks CLI로 앱 생성")
    print("   databricks apps create genie-chatbot")
    print()
    print("   # 앱 배포")
    print("   databricks apps deploy genie-chatbot --source-code-path .")
    print()
    print("   # 배포 상태 확인")
    print("   databricks apps get genie-chatbot")


if __name__ == "__main__":
    main()
